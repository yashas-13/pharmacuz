from flask import Blueprint, jsonify
from sqlalchemy.orm import Session
from backend.auth import roles_required
from backend.database import SessionLocal
from backend.models.product import Product
from backend.models.batch import Batch

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


@product_bp.route('/batches', methods=['GET'])
@roles_required('manufacturer', 'cfa', 'super_stockist')
def list_batches():
    """Return all batch records for any authenticated role"""
    session: Session = SessionLocal()
    batches = session.query(Batch).all()
    result = [
        {
            'id': b.id,
            'batch_no': b.batch_no,
            'product_id': b.product_id,
            'mfg_date': str(b.mfg_date) if b.mfg_date else None,
            'exp_date': str(b.exp_date) if b.exp_date else None,
            'mrp': b.mrp,
            'quantity': b.quantity,
        }
        for b in batches
    ]
    session.close()
    return jsonify(result)
