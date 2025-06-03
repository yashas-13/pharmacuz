from flask import Blueprint, request, jsonify
from auth import role_required

manufacturer_bp = Blueprint('manufacturer', __name__)

# In-memory product storage
PRODUCTS = []

@manufacturer_bp.route('/products', methods=['GET', 'POST'])
@role_required('manufacturer')
def products():
    if request.method == 'POST':
        data = request.json or {}
        name = data.get('name')
        if not name:
            return jsonify({'error': 'Invalid product data'}), 400
        product = {
            'id': len(PRODUCTS) + 1,
            'name': name
        }
        PRODUCTS.append(product)
        return jsonify(product), 201
    return jsonify(PRODUCTS)
