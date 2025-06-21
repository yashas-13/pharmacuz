from flask import Blueprint, request, jsonify
from .auth import role_required
from ..models import db
from ..models.product import Product
from ..models.order import Order
from ..models.grn import GRN

manufacturer_bp = Blueprint('manufacturer', __name__)

@manufacturer_bp.route('/products', methods=['GET', 'POST'])
@role_required('manufacturer')
def products():
    if request.method == 'POST':
        data = request.get_json() or {}
        name = data.get('name')
        quantity = data.get('quantity', 0)
        warehouse = data.get('warehouse')
        if not name:
            return jsonify({'error': 'Invalid product data'}), 400
        product = Product(name=name, quantity=quantity, warehouse=warehouse)
        db.session.add(product)
        db.session.commit()
        return jsonify({'id': product.id, 'name': product.name}), 201
    products = Product.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'quantity': p.quantity} for p in products])

@manufacturer_bp.route('/analytics/orders', methods=['GET'])
@role_required('manufacturer')
def order_analytics():
    # Return dummy analytics data
    return jsonify({
        'daily': 120,
        'weekly': 840,
        'monthly': 3200
    })

@manufacturer_bp.route('/recall', methods=['POST'])
@role_required('manufacturer')
def recall():
    data = request.get_json() or {}
    batch = data.get('batch')
    reason = data.get('reason')
    if not batch or not reason:
        return jsonify({'error': 'Invalid recall data'}), 400
    # In a real app we would notify stockists here
    return jsonify({'status': 'initiated', 'batch': batch})

@manufacturer_bp.route('/schemes', methods=['GET'])
@role_required('manufacturer')
def schemes():
    return jsonify([
        {'id': 1, 'name': 'Buy One Get One'},
        {'id': 2, 'name': 'Summer Discount'}
    ])
