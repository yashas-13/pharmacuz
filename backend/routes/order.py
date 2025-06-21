from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from datetime import date
from backend.auth import role_required, roles_required
from backend.database import SessionLocal
from backend.models.order import Order
from backend.models.product import Product
from backend.models.inventory import Inventory
from backend.models.batch import Batch
from backend.models.audit_log import AuditLog


def _parse_iso_date(value):
    if isinstance(value, str) and value:
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None
    return value


def log_event(session: Session, event_type: str, details: str):
    """Create an audit log entry including user context."""
    username = getattr(request, 'user', {}).get('username') if hasattr(request, 'user') else None
    role = getattr(request, 'user', {}).get('role') if hasattr(request, 'user') else None
    log = AuditLog(event_type=event_type, details=details, username=username, role=role)
    session.add(log)
    session.commit()

order_bp = Blueprint('order', __name__)

@order_bp.route('/orders', methods=['GET', 'POST'])
@roles_required('super_stockist', 'manufacturer', 'cfa')
def orders():
    session: Session = SessionLocal()
    if request.method == 'POST':
        user_role = request.user['role']
        if user_role not in ('super_stockist', 'cfa'):
            session.close()
            return jsonify({'error': 'Forbidden'}), 403
        data = request.json or {}
        product = data.get('product')
        quantity = data.get('quantity')
        if not product or quantity is None:
            session.close()
            return jsonify({'error': 'Invalid order data'}), 400
        target = 'cfa' if user_role == 'super_stockist' else 'manufacturer'
        order = Order(
            product=product,
            quantity=quantity,
            status='created',
            placed_by=request.user['username'],
            target=target,
            order_date=date.today()
        )
        session.add(order)
        session.commit()
        log_event(session, 'order_created', f'Order {order.id} created by {request.user["username"]}')
        result = {
            'id': order.id,
            'product': order.product,
            'quantity': order.quantity,
            'status': order.status,
            'placed_by': order.placed_by,
            'target': order.target,
            'batch_no': order.batch_no,
            'mfg_date': str(order.mfg_date) if order.mfg_date else None,
            'exp_date': str(order.exp_date) if order.exp_date else None,
            'order_date': str(order.order_date)
        }
        session.close()
        return jsonify(result), 201

    status = request.args.get('status')
    target_filter = request.args.get('target')
    query = session.query(Order)
    if status:
        query = query.filter(Order.status == status)
    if target_filter:
        query = query.filter(Order.target == target_filter)
    orders = query.all()
    result = [
        {
            'id': o.id,
            'product': o.product,
            'quantity': o.quantity,
            'status': o.status,
            'placed_by': o.placed_by,
            'target': o.target,
            'batch_no': o.batch_no,
            'mfg_date': str(o.mfg_date) if o.mfg_date else None,
            'exp_date': str(o.exp_date) if o.exp_date else None,
            'order_date': str(o.order_date)
        }
        for o in orders
    ]
    session.close()
    return jsonify(result)


@order_bp.route('/orders/<int:order_id>/request-approval', methods=['POST'])
@role_required('cfa')
def request_approval(order_id):
    """CFA forwards order to manufacturer for approval."""
    session: Session = SessionLocal()
    order = session.query(Order).get(order_id)
    if not order:
        session.close()
        return jsonify({'error': 'Order not found'}), 404
    if order.status != 'created':
        session.close()
        return jsonify({'error': 'Order cannot be forwarded'}), 400
    order.status = 'approval_requested'
    order.target = 'manufacturer'
    session.commit()
    log_event(session, 'order_forwarded', f'Order {order.id} sent for approval')
    result = {
        'id': order.id,
        'product': order.product,
        'quantity': order.quantity,
        'status': order.status,
        'placed_by': order.placed_by,
        'target': order.target,
        'order_date': str(order.order_date)
    }
    session.close()
    return jsonify(result)


@order_bp.route('/orders/<int:order_id>/approve', methods=['POST'])
@role_required('manufacturer')
def approve_order(order_id):
    """Manufacturer approves an order."""
    session: Session = SessionLocal()
    order = session.query(Order).get(order_id)
    if not order:
        session.close()
        return jsonify({'error': 'Order not found'}), 404
    if order.status not in ('created', 'approval_requested'):
        session.close()
        return jsonify({'error': 'Order cannot be approved'}), 400
    order.status = 'approved'
    session.commit()
    log_event(session, 'order_approved', f'Order {order.id} approved')
    result = {
        'id': order.id,
        'product': order.product,
        'quantity': order.quantity,
        'status': order.status,
        'batch_no': order.batch_no,
        'mfg_date': str(order.mfg_date) if order.mfg_date else None,
        'exp_date': str(order.exp_date) if order.exp_date else None,
        'placed_by': order.placed_by,
        'target': order.target,
        'order_date': str(order.order_date)
    }
    session.close()
    return jsonify(result)


@order_bp.route('/orders/<int:order_id>/dispatch', methods=['POST'])
@roles_required('cfa', 'manufacturer')
def dispatch_order(order_id):
    """Dispatch an approved order with batch details."""
    session: Session = SessionLocal()
    order = session.query(Order).get(order_id)
    if not order:
        session.close()
        return jsonify({'error': 'Order not found'}), 404
    if order.status != 'approved':
        session.close()
        return jsonify({'error': 'Order cannot be dispatched'}), 400

    data = request.json or {}
    batch_no = data.get('batch_no')
    mfg_date = _parse_iso_date(data.get('mfg_date'))
    exp_date = _parse_iso_date(data.get('exp_date'))
    if not batch_no:
        session.close()
        return jsonify({'error': 'batch_no required'}), 400

    product = session.query(Product).filter_by(name=order.product).first()
    if not product:
        session.close()
        return jsonify({'error': 'Product not found'}), 400

    if not session.query(Batch).filter_by(product_id=product.id, batch_no=batch_no).first():
        session.close()
        return jsonify({'error': 'Invalid batch for product'}), 400

    inventory = session.query(Inventory).filter_by(
        location=request.user['username'],
        product_id=product.id,
        batch_no=batch_no
    ).first()
    if not inventory or inventory.quantity < order.quantity:
        session.close()
        return jsonify({'error': 'Insufficient stock'}), 400

    inventory.quantity -= order.quantity
    log_event(session, 'inventory_deducted', f'{order.quantity} units of product {product.id} batch {batch_no} deducted from {inventory.location}')

    order.status = 'dispatched'
    order.batch_no = batch_no
    order.mfg_date = mfg_date
    order.exp_date = exp_date
    session.commit()
    log_event(session, 'order_dispatched', f'Order {order.id} dispatched with batch {batch_no}')
    result = {
        'id': order.id,
        'product': order.product,
        'quantity': order.quantity,
        'status': order.status,
        'batch_no': order.batch_no,
        'mfg_date': str(order.mfg_date) if order.mfg_date else None,
        'exp_date': str(order.exp_date) if order.exp_date else None,
        'placed_by': order.placed_by,
        'target': order.target,
        'order_date': str(order.order_date)
    }
    session.close()
    return jsonify(result)


@order_bp.route('/orders/<int:order_id>/receive', methods=['POST'])
@roles_required('cfa', 'super_stockist')
def receive_order(order_id):
    """Receiver confirms delivery of an order."""
    session: Session = SessionLocal()
    order = session.query(Order).get(order_id)
    if not order:
        session.close()
        return jsonify({'error': 'Order not found'}), 404
    if order.status != 'dispatched':
        session.close()
        return jsonify({'error': 'Order cannot be received'}), 400
    product = session.query(Product).filter_by(name=order.product).first()
    if product:
        inventory = session.query(Inventory).filter_by(
            location=request.user['username'],
            product_id=product.id,
            batch_no=order.batch_no
        ).first()
        if inventory:
            inventory.quantity += order.quantity
            log_event(session, 'inventory_added', f'{order.quantity} units of product {product.id} batch {order.batch_no} received at {inventory.location}')
        else:
            inventory = Inventory(
                location=request.user['username'],
                product_id=product.id,
                batch_no=order.batch_no,
                mfg_date=order.mfg_date,
                exp_date=order.exp_date,
                quantity=order.quantity
            )
            session.add(inventory)
            log_event(session, 'inventory_added', f'{order.quantity} units of product {product.id} batch {order.batch_no} added to {inventory.location}')
    order.status = 'received'
    session.commit()
    log_event(session, 'order_received', f'Order {order.id} received by {request.user["username"]}')
    result = {
        'id': order.id,
        'product': order.product,
        'quantity': order.quantity,
        'status': order.status,
        'batch_no': order.batch_no,
        'placed_by': order.placed_by,
        'target': order.target,
        'order_date': str(order.order_date)
    }
    session.close()
    return jsonify(result)


@order_bp.route('/orders/<int:order_id>/acknowledge', methods=['POST'])
@roles_required('cfa', 'super_stockist')
def acknowledge_order(order_id):
    """Finalize order after verifying receipt."""
    session: Session = SessionLocal()
    order = session.query(Order).get(order_id)
    if not order:
        session.close()
        return jsonify({'error': 'Order not found'}), 404
    if order.status != 'received':
        session.close()
        return jsonify({'error': 'Order cannot be acknowledged'}), 400
    order.status = 'acknowledged'
    session.commit()
    log_event(session, 'order_acknowledged', f'Order {order.id} acknowledged by {request.user["username"]}')
    result = {
        'id': order.id,
        'product': order.product,
        'quantity': order.quantity,
        'status': order.status,
        'batch_no': order.batch_no,
        'placed_by': order.placed_by,
        'target': order.target,
        'order_date': str(order.order_date)
    }
    session.close()
    return jsonify(result)
