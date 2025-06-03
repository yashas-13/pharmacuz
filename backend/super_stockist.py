from flask import Blueprint, request, jsonify
from .auth import role_required

super_stockist_bp = Blueprint('super_stockist', __name__)

# In-memory stock request storage
REQUESTS = []

@super_stockist_bp.route('/requests', methods=['GET', 'POST'])
@role_required('super_stockist')
def requests_endpoint():
    if request.method == 'POST':
        data = request.json or {}
        product = data.get('product')
        qty = data.get('quantity')
        if not product or not qty:
            return jsonify({'error': 'Invalid request data'}), 400
        req = {
            'id': len(REQUESTS) + 1,
            'product': product,
            'quantity': qty
        }
        REQUESTS.append(req)
        return jsonify(req), 201
    return jsonify(REQUESTS)
