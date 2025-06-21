from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from datetime import date
from backend.auth import role_required, roles_required
from backend.database import SessionLocal
from backend.models.order import Order
from backend.models.product import Product
from backend.models.inventory import Inventory

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
            status='requested',
            placed_by=request.user['username'],
            target=target,
            order_date=date.today()
        )
        session.add(order)
        session.commit()
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
    if order.status != 'requested':
        session.close()
        return jsonify({'error': 'Order cannot be forwarded'}), 400
    order.status = 'approval_requested'
    order.target = 'manufacturer'
    session.commit()
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
    if order.status != 'approval_requested':
        session.close()
        return jsonify({'error': 'Order cannot be approved'}), 400
    order.status = 'approved'
    session.commit()
    result = {
        'id': order.id,
        'product': order.product,
        'quantity': order.quantity,
        'status': order.status
    }
    session.close()
    return jsonify(result)


@order_bp.route('/orders/<int:order_id>/dispatch', methods=['POST'])
@roles_required('cfa', 'manufacturer')
def dispatch_order(order_id):
    """Dispatch an approved order."""
    session: Session = SessionLocal()
    order = session.query(Order).get(order_id)
    if not order:
        session.close()
        return jsonify({'error': 'Order not found'}), 404
    if order.status != 'approved':
        session.close()
        return jsonify({'error': 'Order cannot be dispatched'}), 400
    order.status = 'in_transit'
    session.commit()
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


@order_bp.route('/orders/<int:order_id>/deliver', methods=['POST'])
@role_required('super_stockist')
def deliver_order(order_id):
    """Stockist confirms delivery of an order."""
    session: Session = SessionLocal()
    order = session.query(Order).get(order_id)
    if not order:
        session.close()
        return jsonify({'error': 'Order not found'}), 404
    if order.status != 'in_transit':
        session.close()
        return jsonify({'error': 'Order cannot be marked delivered'}), 400
    order.status = 'delivered'
    # Add delivered quantity to stockist inventory
    product = session.query(Product).filter_by(name=order.product).first()
    if product:
        inventory = Inventory(
            location=request.user['username'],
            product_id=product.id,
            batch_no='N/A',
            exp_date=None,
            quantity=order.quantity
        )
        session.add(inventory)
    session.commit()
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
