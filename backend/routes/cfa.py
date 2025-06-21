from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from backend.auth import role_required
from backend.database import SessionLocal
from backend.models.grn import GRN

cfa_bp = Blueprint('cfa', __name__)

@cfa_bp.route('/grn', methods=['GET', 'POST'])
@role_required('cfa')
def grn():
    session: Session = SessionLocal()
    if request.method == 'POST':
        data = request.json or {}
        batch = data.get('batch')
        quantity = data.get('quantity')
        if not batch or quantity is None:
            session.close()
            return jsonify({'error': 'Invalid GRN data'}), 400
        record = GRN(batch=batch, quantity=quantity)
        session.add(record)
        session.commit()
        result = {'id': record.id, 'batch': record.batch, 'quantity': record.quantity}
        session.close()
        return jsonify(result), 201
    grns = session.query(GRN).all()
    result = [{'id': g.id, 'batch': g.batch, 'quantity': g.quantity} for g in grns]
    session.close()
    return jsonify(result)
