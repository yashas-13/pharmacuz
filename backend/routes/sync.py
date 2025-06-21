from flask import Blueprint, jsonify
from sqlalchemy.orm import Session
from backend.auth import roles_required
from backend.database import SessionLocal
from backend.models.order import Order
from backend.models.inventory import Inventory
from backend.models.product import Product

sync_bp = Blueprint('sync', __name__)

@sync_bp.route('/sync/erp', methods=['GET'])
@roles_required('manufacturer', 'cfa', 'super_stockist')
def erp_sync():
    session: Session = SessionLocal()
    orders = session.query(Order).all()
    inv = session.query(Inventory).join(Product, Inventory.product_id == Product.id).all()
    order_data = [
        {
            'id': o.id,
            'product': o.product,
            'quantity': o.quantity,
            'status': o.status,
            'batch_no': o.batch_no,
            'order_date': str(o.order_date)
        }
        for o in orders
    ]
    inv_data = [
        {
            'id': i.id,
            'location': i.location,
            'product_id': i.product_id,
            'batch_no': i.batch_no,
            'quantity': i.quantity,
            'exp_date': str(i.exp_date) if i.exp_date else None
        }
        for i in inv
    ]
    session.close()
    return jsonify({'orders': order_data, 'inventory': inv_data})

