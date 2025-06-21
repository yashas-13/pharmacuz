from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from backend.auth import role_required, roles_required
from backend.database import SessionLocal
from backend.models.pack_config import PackConfig
from backend.models.audit_log import AuditLog


def log_event(session: Session, event_type: str, details: str):
    username = getattr(request, 'user', {}).get('username') if hasattr(request, 'user') else None
    role = getattr(request, 'user', {}).get('role') if hasattr(request, 'user') else None
    log = AuditLog(event_type=event_type, details=details, username=username, role=role)
    session.add(log)
    session.commit()


pack_config_bp = Blueprint('pack_config', __name__)


@pack_config_bp.route('/pack-configs', methods=['GET'])
@roles_required('manufacturer', 'cfa', 'super_stockist')
def list_configs():
    session: Session = SessionLocal()
    configs = session.query(PackConfig).all()
    result = [
        {
            'id': c.id,
            'product_id': c.product_id,
            'pack_type': c.pack_type,
            'units_per_pack': c.units_per_pack,
            'dimensions': c.dimensions,
        }
        for c in configs
    ]
    session.close()
    return jsonify(result)


@pack_config_bp.route('/pack-configs', methods=['POST'])
@role_required('manufacturer')
def add_config():
    session: Session = SessionLocal()
    data = request.json or {}
    product_id = data.get('product_id')
    pack_type = data.get('pack_type')
    if not product_id or not pack_type:
        session.close()
        return jsonify({'error': 'Invalid pack config data'}), 400
    config = PackConfig(
        product_id=product_id,
        pack_type=pack_type,
        units_per_pack=data.get('units_per_pack'),
        dimensions=data.get('dimensions'),
    )
    session.add(config)
    session.commit()
    log_event(session, 'pack_config_created', f'Pack config {config.id} created')
    result = {
        'id': config.id,
        'product_id': config.product_id,
        'pack_type': config.pack_type,
        'units_per_pack': config.units_per_pack,
        'dimensions': config.dimensions,
    }
    session.close()
    return jsonify(result), 201


@pack_config_bp.route('/pack-configs/<int:config_id>', methods=['PUT', 'DELETE'])
@role_required('manufacturer')
def modify_config(config_id: int):
    session: Session = SessionLocal()
    config = session.query(PackConfig).get(config_id)
    if not config:
        session.close()
        return jsonify({'error': 'Pack config not found'}), 404
    if request.method == 'DELETE':
        session.delete(config)
        session.commit()
        log_event(session, 'pack_config_deleted', f'Pack config {config_id} deleted')
        session.close()
        return jsonify({'message': 'deleted'})
    data = request.json or {}
    config.product_id = data.get('product_id', config.product_id)
    config.pack_type = data.get('pack_type', config.pack_type)
    config.units_per_pack = data.get('units_per_pack', config.units_per_pack)
    config.dimensions = data.get('dimensions', config.dimensions)
    session.commit()
    log_event(session, 'pack_config_updated', f'Pack config {config_id} updated')
    result = {
        'id': config.id,
        'product_id': config.product_id,
        'pack_type': config.pack_type,
        'units_per_pack': config.units_per_pack,
        'dimensions': config.dimensions,
    }
    session.close()
    return jsonify(result)
