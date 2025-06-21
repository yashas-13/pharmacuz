from flask import Blueprint, jsonify, request
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.auth import roles_required, role_required
from backend.database import SessionLocal
from backend.models.order import Order
from backend.models.inventory import Inventory
from backend.models.product import Product

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics/order-stats', methods=['GET'])
@roles_required('manufacturer', 'cfa', 'super_stockist')
def order_stats():
    session: Session = SessionLocal()
    rows = session.query(Order.status, func.count(Order.id)).group_by(Order.status).all()
    result = {status: count for status, count in rows}
    session.close()
    return jsonify(result)

@analytics_bp.route('/analytics/low-stock', methods=['GET'])
@roles_required('manufacturer', 'cfa', 'super_stockist')
def low_stock():
    session: Session = SessionLocal()
    threshold = int(request.args.get('threshold', 50))
    query = session.query(Inventory, Product.name).join(Product, Inventory.product_id == Product.id)
    query = query.filter(Inventory.quantity < threshold)
    if request.user['role'] in ('cfa', 'super_stockist'):
        query = query.filter(Inventory.location == request.user['username'])
    rows = query.all()
    result = [
        {
            'product_name': name,
            'location': inv.location,
            'quantity': inv.quantity
        }
        for inv, name in rows
    ]
    session.close()
    return jsonify(result)

@analytics_bp.route('/analytics/refill-suggestions', methods=['GET'])
@roles_required('manufacturer', 'cfa', 'super_stockist')
def refill_suggestions():
    session: Session = SessionLocal()
    query = session.query(Inventory, Product.name).join(Product, Inventory.product_id == Product.id)
    if request.user['role'] in ('cfa', 'super_stockist'):
        query = query.filter(Inventory.location == request.user['username'])
    rows = query.all()
    suggestions = []
    for inv, name in rows:
        if inv.quantity < 30:
            suggestions.append({'product_name': name, 'suggested_qty': 100 - inv.quantity})
    session.close()
    return jsonify(suggestions)

@analytics_bp.route('/analytics/my-sales', methods=['GET'])
@role_required('super_stockist')
def my_sales():
    session: Session = SessionLocal()
    orders = session.query(Order).filter_by(placed_by=request.user['username'], status='acknowledged').all()
    stats = {}
    for o in orders:
        if o.order_date:
            key = o.order_date.strftime('%Y-%m')
        else:
            key = 'unknown'
        stats[key] = stats.get(key, 0) + o.quantity
    result = [{'month': k, 'sales': v} for k, v in sorted(stats.items())]
    session.close()
    return jsonify(result)
