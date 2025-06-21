from datetime import date
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.auth import role_required, roles_required
from backend.database import SessionLocal
from backend.models.inventory import Inventory
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

inventory_bp = Blueprint('inventory', __name__)


@inventory_bp.route('/inventory', methods=['GET'])
@roles_required('manufacturer', 'cfa', 'super_stockist')
def list_inventory():
    """Return inventory records.

    - Manufacturer can view all locations, optionally filtering by ``location``
      query param.
    - CFA and Super Stockist only view inventory at their own location
      (their username).
    """
    session: Session = SessionLocal()
    query = session.query(Inventory, Product.name).join(Product, Inventory.product_id == Product.id)

    user_role = request.user['role']
    if user_role in ('cfa', 'super_stockist'):
        query = query.filter(Inventory.location == request.user['username'])
    else:
        location_filter = request.args.get('location')
        if location_filter:
            query = query.filter(Inventory.location == location_filter)

    rows = query.all()
    result = []
    for inv, name in rows:
        result.append({
            'id': inv.id,
            'location': inv.location,
            'product_id': inv.product_id,
            'product_name': name,
            'batch_no': inv.batch_no,
            'mfg_date': str(inv.mfg_date) if inv.mfg_date else None,
            'exp_date': str(inv.exp_date) if inv.exp_date else None,
            'quantity': inv.quantity,
            'low_stock': inv.quantity < 50
        })
    session.close()
    return jsonify(result)


@inventory_bp.route('/inventory', methods=['POST'])
@roles_required('cfa', 'super_stockist')
def add_inventory():
    session: Session = SessionLocal()
    data = request.json or {}
    product_id = data.get('product_id')
    batch_no = data.get('batch_no')
    quantity = data.get('quantity')
    if not product_id or not batch_no or quantity is None:
        session.close()
        return jsonify({'error': 'Invalid inventory data'}), 400
    mfg_date = _parse_iso_date(data.get('mfg_date'))
    exp_date = _parse_iso_date(data.get('exp_date'))
    location = data.get('location') or request.user['username']
    inventory = Inventory(
        location=location,
        product_id=product_id,
        batch_no=batch_no,
        mfg_date=mfg_date,
        exp_date=exp_date,
        quantity=quantity
    )
    session.add(inventory)
    session.commit()
    log_event(session, 'inventory_added', f'{quantity} units of product {product_id} batch {batch_no} added to {location}')
    result = {
        'id': inventory.id,
        'location': inventory.location,
        'product_id': inventory.product_id,
        'batch_no': inventory.batch_no,
        'mfg_date': str(inventory.mfg_date) if inventory.mfg_date else None,
        'exp_date': str(inventory.exp_date) if inventory.exp_date else None,
        'quantity': inventory.quantity
    }
    session.close()
    return jsonify(result), 201


@inventory_bp.route('/inventory/reconcile', methods=['GET'])
@roles_required('manufacturer', 'cfa', 'super_stockist')
def reconcile_inventory():
    session: Session = SessionLocal()
    rows = session.query(
        Inventory.product_id,
        Inventory.batch_no,
        func.sum(Inventory.quantity)
    ).group_by(Inventory.product_id, Inventory.batch_no).all()
    result = [
        {
            'product_id': pid,
            'batch_no': batch,
            'total_quantity': qty
        }
        for pid, batch, qty in rows
    ]
    session.close()
    return jsonify(result)
