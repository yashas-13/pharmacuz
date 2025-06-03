from flask import Blueprint, request, jsonify
from auth import role_required

cfa_bp = Blueprint('cfa', __name__)

# In-memory GRN storage
GRNS = []

@cfa_bp.route('/grn', methods=['GET', 'POST'])
@role_required('cfa')
def grn():
    if request.method == 'POST':
        data = request.json or {}
        batch = data.get('batch')
        quantity = data.get('quantity')
        if not batch or not quantity:
            return jsonify({'error': 'Invalid GRN data'}), 400
        record = {
            'id': len(GRNS) + 1,
            'batch': batch,
            'quantity': quantity
        }
        GRNS.append(record)
        return jsonify(record), 201
    return jsonify(GRNS)
