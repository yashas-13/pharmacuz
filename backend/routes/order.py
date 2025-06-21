from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from backend.auth import role_required
from backend.database import SessionLocal
from backend.models.order import Order

order_bp = Blueprint('order', __name__)

@order_bp.route('/orders', methods=['GET', 'POST'])
@role_required('super_stockist')
def orders():
    session: Session = SessionLocal()
    if request.method == 'POST':
        data = request.json or {}
        product = data.get('product')
        quantity = data.get('quantity')
        if not product or quantity is None:
            session.close()
            return jsonify({'error': 'Invalid order data'}), 400
        order = Order(product=product, quantity=quantity, status='requested')
        session.add(order)
        session.commit()
        result = {'id': order.id, 'product': order.product, 'quantity': order.quantity, 'status': order.status}
        session.close()
        return jsonify(result), 201
    orders = session.query(Order).all()
    result = [{'id': o.id, 'product': o.product, 'quantity': o.quantity, 'status': o.status} for o in orders]
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
    if order.status != 'requested':
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
@role_required('cfa')
def dispatch_order(order_id):
    """CFA dispatches an approved order."""
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
        'status': order.status
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
    session.commit()
    result = {
        'id': order.id,
        'product': order.product,
        'quantity': order.quantity,
        'status': order.status
    }
    session.close()
    return jsonify(result)
