from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from backend.auth import role_required
from backend.database import SessionLocal
from backend.models.cfa_stock_movement import CFAStockMovement
from backend.models.audit_log import AuditLog


def log_event(session: Session, event_type: str, details: str):
    username = getattr(request, 'user', {}).get('username') if hasattr(request, 'user') else None
    role = getattr(request, 'user', {}).get('role') if hasattr(request, 'user') else None
    log = AuditLog(event_type=event_type, details=details, username=username, role=role)
    session.add(log)
    session.commit()


cfa_stock_bp = Blueprint('cfa_stock', __name__)


@cfa_stock_bp.route('/cfa/stock', methods=['GET', 'POST'])
@role_required('cfa')
def stock_movements():
    session: Session = SessionLocal()
    if request.method == 'POST':
        data = request.json or {}
        product_id = data.get('product_id')
        batch_no = data.get('batch_no')
        quantity = data.get('quantity')
        action = data.get('action')
        if not product_id or not batch_no or quantity is None or action not in ('received', 'dispatched'):
            session.close()
            return jsonify({'error': 'Invalid stock movement data'}), 400
        movement = CFAStockMovement(
            cfa=request.user['username'],
            product_id=product_id,
            batch_no=batch_no,
            quantity=quantity,
            action=action
        )
        session.add(movement)
        session.commit()
        log_event(session, f'cfa_stock_{action}', f'{quantity} units {action} for product {product_id} batch {batch_no}')
        result = {
            'id': movement.id,
            'cfa': movement.cfa,
            'product_id': movement.product_id,
            'batch_no': movement.batch_no,
            'quantity': movement.quantity,
            'action': movement.action,
            'timestamp': movement.timestamp.isoformat()
        }
        session.close()
        return jsonify(result), 201

    query = session.query(CFAStockMovement).filter(CFAStockMovement.cfa == request.user['username'])
    action_filter = request.args.get('action')
    if action_filter:
        query = query.filter(CFAStockMovement.action == action_filter)
    movements = query.order_by(CFAStockMovement.timestamp.desc()).all()
    result = [
        {
            'id': m.id,
            'cfa': m.cfa,
            'product_id': m.product_id,
            'batch_no': m.batch_no,
            'quantity': m.quantity,
            'action': m.action,
            'timestamp': m.timestamp.isoformat()
        }
        for m in movements
    ]
    session.close()
    return jsonify(result)
