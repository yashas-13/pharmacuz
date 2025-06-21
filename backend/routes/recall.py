from datetime import date
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from backend.auth import role_required, roles_required
from backend.database import SessionLocal
from backend.models.recall import Recall
from backend.models.product import Product
from backend.models.batch import Batch
from backend.models.audit_log import AuditLog

recall_bp = Blueprint('recall', __name__)


def log_event(session: Session, event_type: str, details: str):
    username = getattr(request, 'user', {}).get('username') if hasattr(request, 'user') else None
    role = getattr(request, 'user', {}).get('role') if hasattr(request, 'user') else None
    log = AuditLog(event_type=event_type, details=details, username=username, role=role)
    session.add(log)
    session.commit()


@recall_bp.route('/recalls', methods=['GET'])
@roles_required('manufacturer', 'cfa', 'super_stockist')
def list_recalls():
    session: Session = SessionLocal()
    status = request.args.get('status')
    query = session.query(Recall, Batch.product_id, Product.name).\
        join(Batch, Recall.batch_no == Batch.batch_no).\
        join(Product, Batch.product_id == Product.id)
    if status:
        query = query.filter(Recall.status == status)
    rows = query.all()
    result = []
    for r, product_id, product_name in rows:
        result.append({
            'id': r.id,
            'batch_no': r.batch_no,
            'product_id': product_id,
            'product_name': product_name,
            'reason': r.reason,
            'start_date': str(r.start_date),
            'status': r.status
        })
    session.close()
    return jsonify(result)


@recall_bp.route('/recalls', methods=['POST'])
@role_required('manufacturer')
def create_recall():
    session: Session = SessionLocal()
    data = request.json or {}
    batch_no = data.get('batch_no')
    reason = data.get('reason')
    if not batch_no or not reason:
        session.close()
        return jsonify({'error': 'Invalid recall data'}), 400
    recall = Recall(batch_no=batch_no, reason=reason, start_date=date.today(), status='active')
    session.add(recall)
    session.commit()
    log_event(session, 'recall_created', f'Recall {recall.id} started for batch {batch_no}')
    result = {
        'id': recall.id,
        'batch_no': recall.batch_no,
        'reason': recall.reason,
        'start_date': str(recall.start_date),
        'status': recall.status
    }
    session.close()
    return jsonify(result), 201


@recall_bp.route('/recalls/<int:recall_id>', methods=['PUT'])
@role_required('manufacturer')
def update_recall(recall_id: int):
    session: Session = SessionLocal()
    recall = session.query(Recall).get(recall_id)
    if not recall:
        session.close()
        return jsonify({'error': 'Recall not found'}), 404
    data = request.json or {}
    if 'status' in data:
        recall.status = data['status']
    if 'reason' in data:
        recall.reason = data['reason']
    session.commit()
    log_event(session, 'recall_updated', f'Recall {recall_id} updated')
    result = {
        'id': recall.id,
        'batch_no': recall.batch_no,
        'reason': recall.reason,
        'start_date': str(recall.start_date),
        'status': recall.status
    }
    session.close()
    return jsonify(result)
