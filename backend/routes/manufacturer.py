from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from backend.auth import role_required
from backend.database import SessionLocal
from backend.models.product import Product

manufacturer_bp = Blueprint('manufacturer', __name__)

@manufacturer_bp.route('/products', methods=['GET', 'POST'])
@role_required('manufacturer')
def products():
    session: Session = SessionLocal()
    if request.method == 'POST':
        data = request.json or {}
        name = data.get('name')
        if not name:
            session.close()
            return jsonify({'error': 'Invalid product data'}), 400
        product = Product(
            name=name,
            hsn=data.get('hsn'),
            gst=data.get('gst'),
            composition=data.get('composition'),
            category=data.get('category')
        )
        session.add(product)
        session.commit()
        result = {
            'id': product.id,
            'name': product.name,
            'hsn': product.hsn,
            'gst': product.gst,
            'composition': product.composition,
            'category': product.category
        }
        session.close()
        return jsonify(result), 201
    products = session.query(Product).all()
    result = [
        {
            'id': p.id,
            'name': p.name,
            'hsn': p.hsn,
            'gst': p.gst,
            'composition': p.composition,
            'category': p.category
        } for p in products
    ]
    session.close()
    return jsonify(result)
