from datetime import date
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from backend.auth import roles_required, role_required
from backend.database import SessionLocal
from backend.models.pricing_catalog import PricingCatalog
from backend.models.product import Product
from backend.models.audit_log import AuditLog


def _parse_iso_date(value):
    if isinstance(value, str) and value:
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None
    return value


def log_event(session: Session, event_type: str, details: str):
    username = getattr(request, 'user', {}).get('username') if hasattr(request, 'user') else None
    role = getattr(request, 'user', {}).get('role') if hasattr(request, 'user') else None
    log = AuditLog(event_type=event_type, details=details, username=username, role=role)
    session.add(log)
    session.commit()


pricing_bp = Blueprint('pricing', __name__)


@pricing_bp.route('/pricing', methods=['GET'])
@roles_required('manufacturer', 'cfa', 'super_stockist')
def list_pricing():
    session: Session = SessionLocal()
    region = request.args.get('region')
    query = session.query(PricingCatalog, Product.name).join(Product, PricingCatalog.product_id == Product.id)
    if region and region != 'all':
        query = query.filter(PricingCatalog.region == region)
    rows = query.all()
    result = []
    for p, name in rows:
        result.append({
            'id': p.id,
            'product_id': p.product_id,
            'product_name': name,
            'region': p.region,
            'ptr': p.ptr,
            'pts': p.pts,
            'effective_date': str(p.effective_date)
        })
    session.close()
    return jsonify(result)


@pricing_bp.route('/pricing', methods=['POST'])
@role_required('manufacturer')
def add_pricing():
    session: Session = SessionLocal()
    data = request.json or {}
    product_id = data.get('product_id')
    region = data.get('region')
    ptr = data.get('ptr')
    pts = data.get('pts')
    effective_date = _parse_iso_date(data.get('effective_date'))
    if not product_id or not region or ptr is None or pts is None or not effective_date:
        session.close()
        return jsonify({'error': 'Invalid pricing data'}), 400
    record = PricingCatalog(
        product_id=product_id,
        region=region,
        ptr=ptr,
        pts=pts,
        effective_date=effective_date
    )
    session.add(record)
    session.commit()
    log_event(session, 'pricing_added', f'Pricing {record.id} added for product {product_id}')
    result = {
        'id': record.id,
        'product_id': record.product_id,
        'region': record.region,
        'ptr': record.ptr,
        'pts': record.pts,
        'effective_date': str(record.effective_date)
    }
    session.close()
    return jsonify(result), 201


@pricing_bp.route('/pricing/<int:pricing_id>', methods=['PUT'])
@role_required('manufacturer')
def update_pricing(pricing_id: int):
    session: Session = SessionLocal()
    record = session.query(PricingCatalog).get(pricing_id)
    if not record:
        session.close()
        return jsonify({'error': 'Pricing not found'}), 404
    data = request.json or {}
    if 'product_id' in data:
        record.product_id = data['product_id']
    if 'region' in data:
        record.region = data['region']
    if 'ptr' in data:
        record.ptr = data['ptr']
    if 'pts' in data:
        record.pts = data['pts']
    if 'effective_date' in data:
        record.effective_date = _parse_iso_date(data['effective_date'])
    session.commit()
    log_event(session, 'pricing_updated', f'Pricing {pricing_id} updated')
    result = {
        'id': record.id,
        'product_id': record.product_id,
        'region': record.region,
        'ptr': record.ptr,
        'pts': record.pts,
        'effective_date': str(record.effective_date)
    }
    session.close()
    return jsonify(result)


@pricing_bp.route('/pricing/<int:pricing_id>', methods=['DELETE'])
@role_required('manufacturer')
def delete_pricing(pricing_id: int):
    session: Session = SessionLocal()
    record = session.query(PricingCatalog).get(pricing_id)
    if not record:
        session.close()
        return jsonify({'error': 'Pricing not found'}), 404
    session.delete(record)
    session.commit()
    log_event(session, 'pricing_deleted', f'Pricing {pricing_id} deleted')
    session.close()
    return jsonify({'message': 'deleted'})
