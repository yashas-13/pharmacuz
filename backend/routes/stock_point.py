from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from backend.auth import role_required
from backend.database import SessionLocal
from backend.models.stock_point import StockPoint
from backend.models.audit_log import AuditLog

stock_point_bp = Blueprint('stock_point', __name__)


def log_event(session: Session, event_type: str, details: str):
    username = getattr(request, 'user', {}).get('username') if hasattr(request, 'user') else None
    role = getattr(request, 'user', {}).get('role') if hasattr(request, 'user') else None
    log = AuditLog(event_type=event_type, details=details, username=username, role=role)
    session.add(log)
    session.commit()


@stock_point_bp.route('/stock-points', methods=['GET', 'POST'])
@role_required('manufacturer')
def manage_stock_points():
    session: Session = SessionLocal()
    if request.method == 'POST':
        data = request.json or {}
        name = data.get('name')
        cfa_username = data.get('cfa_username')
        if not name or not cfa_username:
            session.close()
            return jsonify({'error': 'Invalid stock point data'}), 400
        record = StockPoint(name=name, cfa_username=cfa_username, active=1)
        session.add(record)
        session.commit()
        log_event(session, 'stock_point_created', f'{name} assigned to {cfa_username}')
        result = {
            'id': record.id,
            'name': record.name,
            'cfa_username': record.cfa_username,
            'active': record.active,
        }
        session.close()
        return jsonify(result), 201

    records = session.query(StockPoint).all()
    result = [
        {
            'id': r.id,
            'name': r.name,
            'cfa_username': r.cfa_username,
            'active': r.active,
        }
        for r in records
    ]
    session.close()
    return jsonify(result)


@stock_point_bp.route('/stock-points/<int:sp_id>', methods=['PUT', 'DELETE'])
@role_required('manufacturer')
def modify_stock_point(sp_id: int):
    session: Session = SessionLocal()
    sp = session.query(StockPoint).get(sp_id)
    if not sp:
        session.close()
        return jsonify({'error': 'Stock point not found'}), 404
    if request.method == 'DELETE':
        session.delete(sp)
        session.commit()
        log_event(session, 'stock_point_deleted', f'{sp_id} deleted')
        session.close()
        return jsonify({'message': 'deleted'})
    data = request.json or {}
    if 'name' in data:
        sp.name = data['name']
    if 'cfa_username' in data:
        sp.cfa_username = data['cfa_username']
    if 'active' in data:
        sp.active = data['active']
    session.commit()
    log_event(session, 'stock_point_updated', f'{sp_id} updated')
    result = {
        'id': sp.id,
        'name': sp.name,
        'cfa_username': sp.cfa_username,
        'active': sp.active,
    }
    session.close()
    return jsonify(result)
