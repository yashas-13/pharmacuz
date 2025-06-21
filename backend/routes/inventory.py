from datetime import date
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from backend.auth import role_required, roles_required
from backend.database import SessionLocal
from backend.models.inventory import Inventory
from backend.models.product import Product


def _parse_iso_date(value):
    if isinstance(value, str) and value:
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None
    return value

inventory_bp = Blueprint('inventory', __name__)


@inventory_bp.route('/inventory', methods=['GET'])
@role_required('manufacturer')
def list_inventory():
    session: Session = SessionLocal()
    rows = session.query(Inventory, Product.name).join(Product, Inventory.product_id == Product.id).all()
    result = []
    for inv, name in rows:
        result.append({
            'id': inv.id,
            'location': inv.location,
            'product_id': inv.product_id,
            'product_name': name,
            'batch_no': inv.batch_no,
            'exp_date': str(inv.exp_date) if inv.exp_date else None,
            'quantity': inv.quantity
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
    exp_date = _parse_iso_date(data.get('exp_date'))
    location = data.get('location') or request.user['username']
    inventory = Inventory(
        location=location,
        product_id=product_id,
        batch_no=batch_no,
        exp_date=exp_date,
        quantity=quantity
    )
    session.add(inventory)
    session.commit()
    result = {
        'id': inventory.id,
        'location': inventory.location,
        'product_id': inventory.product_id,
        'batch_no': inventory.batch_no,
        'exp_date': str(inventory.exp_date) if inventory.exp_date else None,
        'quantity': inventory.quantity
    }
    session.close()
    return jsonify(result), 201
