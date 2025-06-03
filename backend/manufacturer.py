from flask import Blueprint, request, jsonify
from .auth import role_required
import json
import os

manufacturer_bp = Blueprint('manufacturer', __name__)

# In-memory product storage loaded from JSON if available
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'products.json')
if os.path.exists(DATA_PATH):
    with open(DATA_PATH) as f:
        PRODUCTS = json.load(f)
    # assign IDs if missing
    for idx, p in enumerate(PRODUCTS, start=1):
        p.setdefault('id', idx)
else:
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
            'id': max([p.get('id', 0) for p in PRODUCTS] or [0]) + 1,
            'name': name
        }
        PRODUCTS.append(product)
        return jsonify(product), 201
    return jsonify(PRODUCTS)
