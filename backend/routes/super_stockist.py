from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from backend.auth import role_required
from backend.database import SessionLocal
from backend.models.stock_request import StockRequest

super_stockist_bp = Blueprint('super_stockist', __name__)

@super_stockist_bp.route('/requests', methods=['GET', 'POST'])
@role_required('super_stockist')
def requests_endpoint():
    session: Session = SessionLocal()
    if request.method == 'POST':
        data = request.json or {}
        product = data.get('product')
        quantity = data.get('quantity')
        if not product or quantity is None:
            session.close()
            return jsonify({'error': 'Invalid request data'}), 400
        req = StockRequest(product=product, quantity=quantity)
        session.add(req)
        session.commit()
        result = {'id': req.id, 'product': req.product, 'quantity': req.quantity}
        session.close()
        return jsonify(result), 201
    requests_list = session.query(StockRequest).all()
    result = [{'id': r.id, 'product': r.product, 'quantity': r.quantity} for r in requests_list]
    session.close()
    return jsonify(result)
