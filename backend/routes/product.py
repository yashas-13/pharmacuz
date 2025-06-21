from flask import Blueprint, jsonify
from sqlalchemy.orm import Session
from backend.auth import roles_required
from backend.database import SessionLocal
from backend.models.product import Product

product_bp = Blueprint('product', __name__)

@product_bp.route('/products', methods=['GET'])
@roles_required('manufacturer', 'cfa', 'super_stockist')
def list_products():
    """Return all products for any authenticated role"""
    session: Session = SessionLocal()
    products = session.query(Product).all()
    result = [
        {
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'hsn': p.hsn,
            'gst': p.gst,
            'composition': p.composition,
            'category': p.category,
        }
        for p in products
    ]
    session.close()
    return jsonify(result)
