from flask import Blueprint, request, jsonify
from .auth import role_required
from ..models import db
from ..models.grn import GRN

cfa_bp = Blueprint('cfa', __name__)

@cfa_bp.route('/grn', methods=['GET', 'POST'])
@role_required('cfa')
def grn():
    if request.method == 'POST':
        data = request.get_json() or {}
        batch = data.get('batch')
        quantity = data.get('quantity')
        if not batch or not quantity:
            return jsonify({'error': 'Invalid GRN data'}), 400
        record = GRN(batch=batch, quantity=quantity)
        db.session.add(record)
        db.session.commit()
        return jsonify({'id': record.id, 'batch': record.batch}), 201
    grns = GRN.query.all()
    return jsonify([{'id': g.id, 'batch': g.batch, 'quantity': g.quantity} for g in grns])

@cfa_bp.route('/tasks', methods=['GET'])
@role_required('cfa')
def tasks():
    return jsonify({
        'to_pack': 5,
        'dispatch': 3,
        'pending': 2
    })
