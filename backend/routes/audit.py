from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from backend.auth import roles_required
from backend.database import SessionLocal
from backend.models.audit_log import AuditLog

audit_bp = Blueprint('audit', __name__)

@audit_bp.route('/audit-logs', methods=['GET'])
@roles_required('manufacturer', 'cfa', 'super_stockist')
def get_logs():
    session: Session = SessionLocal()
    query = session.query(AuditLog)
    role_filter = request.args.get('role')
    user_filter = request.args.get('user')
    if role_filter:
        query = query.filter(AuditLog.role == role_filter)
    if user_filter:
        query = query.filter(AuditLog.username == user_filter)
    logs = query.order_by(AuditLog.timestamp.desc()).limit(100).all()
    result = [
        {
            'id': log.id,
            'event_type': log.event_type,
            'details': log.details,
            'username': log.username,
            'role': log.role,
            'timestamp': log.timestamp.isoformat()
        }
        for log in logs
    ]
    session.close()
    return jsonify(result)

