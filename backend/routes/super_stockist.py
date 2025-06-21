from flask import Blueprint, request, jsonify
from .auth import role_required
from ..models import db
from ..models.stock_request import StockRequest

super_stockist_bp = Blueprint('super_stockist', __name__)

@super_stockist_bp.route('/requests', methods=['GET', 'POST'])
@role_required('super_stockist')
def requests_endpoint():
    if request.method == 'POST':
        data = request.get_json() or {}
        product = data.get('product')
        qty = data.get('quantity')
        if not product or not qty:
            return jsonify({'error': 'Invalid request data'}), 400
        req = StockRequest(product=product, quantity=qty)
        db.session.add(req)
        db.session.commit()
        return jsonify({'id': req.id, 'product': req.product}), 201
    reqs = StockRequest.query.all()
    return jsonify([{'id': r.id, 'product': r.product, 'quantity': r.quantity} for r in reqs])
