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
