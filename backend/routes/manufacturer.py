from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from backend.auth import role_required
from backend.database import SessionLocal
from backend.models.product import Product
from backend.models.batch import Batch
from backend.models.pack_config import PackConfig
from backend.models.user import User

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


@manufacturer_bp.route('/batches', methods=['GET', 'POST'])
@role_required('manufacturer')
def batches():
    session: Session = SessionLocal()
    if request.method == 'POST':
        data = request.json or {}
        batch_no = data.get('batch_no')
        product_id = data.get('product_id')
        if not batch_no or not product_id:
            session.close()
            return jsonify({'error': 'Invalid batch data'}), 400
        mfg_date = data.get('mfg_date')
        exp_date = data.get('exp_date')
        batch = Batch(
            batch_no=batch_no,
            product_id=product_id,
            mfg_date=mfg_date,
            exp_date=exp_date,
            mrp=data.get('mrp'),
            quantity=data.get('quantity')
        )
        session.add(batch)
        session.commit()
        result = {
            'id': batch.id,
            'batch_no': batch.batch_no,
            'product_id': batch.product_id,
            'mfg_date': str(batch.mfg_date) if batch.mfg_date else None,
            'exp_date': str(batch.exp_date) if batch.exp_date else None,
            'mrp': batch.mrp,
            'quantity': batch.quantity
        }
        session.close()
        return jsonify(result), 201
    batches = session.query(Batch).all()
    result = [
        {
            'id': b.id,
            'batch_no': b.batch_no,
            'product_id': b.product_id,
            'mfg_date': str(b.mfg_date) if b.mfg_date else None,
            'exp_date': str(b.exp_date) if b.exp_date else None,
            'mrp': b.mrp,
            'quantity': b.quantity
        } for b in batches
    ]
    session.close()
    return jsonify(result)


@manufacturer_bp.route('/batches/<int:batch_id>', methods=['PUT'])
@role_required('manufacturer')
def update_batch(batch_id):
    session: Session = SessionLocal()
    batch = session.query(Batch).get(batch_id)
    if not batch:
        session.close()
        return jsonify({'error': 'Batch not found'}), 404
    data = request.json or {}
    batch.batch_no = data.get('batch_no', batch.batch_no)
    batch.product_id = data.get('product_id', batch.product_id)
    if 'mfg_date' in data:
        batch.mfg_date = data['mfg_date']
    if 'exp_date' in data:
        batch.exp_date = data['exp_date']
    batch.mrp = data.get('mrp', batch.mrp)
    batch.quantity = data.get('quantity', batch.quantity)
    session.commit()
    result = {
        'id': batch.id,
        'batch_no': batch.batch_no,
        'product_id': batch.product_id,
        'mfg_date': str(batch.mfg_date) if batch.mfg_date else None,
        'exp_date': str(batch.exp_date) if batch.exp_date else None,
        'mrp': batch.mrp,
        'quantity': batch.quantity
    }
    session.close()
    return jsonify(result)


@manufacturer_bp.route('/pack-configs', methods=['GET', 'POST'])
@role_required('manufacturer')
def pack_configs():
    session: Session = SessionLocal()
    if request.method == 'POST':
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
            dimensions=data.get('dimensions')
        )
        session.add(config)
        session.commit()
        result = {
            'id': config.id,
            'product_id': config.product_id,
            'pack_type': config.pack_type,
            'units_per_pack': config.units_per_pack,
            'dimensions': config.dimensions
        }
        session.close()
        return jsonify(result), 201
    configs = session.query(PackConfig).all()
    result = [
        {
            'id': c.id,
            'product_id': c.product_id,
            'pack_type': c.pack_type,
            'units_per_pack': c.units_per_pack,
            'dimensions': c.dimensions
        } for c in configs
    ]
    session.close()
    return jsonify(result)


@manufacturer_bp.route('/pack-configs/<int:config_id>', methods=['PUT'])
@role_required('manufacturer')
def update_pack_config(config_id):
    session: Session = SessionLocal()
    config = session.query(PackConfig).get(config_id)
    if not config:
        session.close()
        return jsonify({'error': 'Pack config not found'}), 404
    data = request.json or {}
    config.product_id = data.get('product_id', config.product_id)
    config.pack_type = data.get('pack_type', config.pack_type)
    config.units_per_pack = data.get('units_per_pack', config.units_per_pack)
    config.dimensions = data.get('dimensions', config.dimensions)
    session.commit()
    result = {
        'id': config.id,
        'product_id': config.product_id,
        'pack_type': config.pack_type,
        'units_per_pack': config.units_per_pack,
        'dimensions': config.dimensions
    }
    session.close()
    return jsonify(result)


@manufacturer_bp.route('/users', methods=['GET', 'POST'])
@role_required('manufacturer')
def manage_users():
    """Create or list CFA and stockist users."""
    session: Session = SessionLocal()
    if request.method == 'POST':
        data = request.json or {}
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        if not username or not password or role not in ('cfa', 'super_stockist'):
            session.close()
            return jsonify({'error': 'Invalid user data'}), 400
        if session.query(User).filter_by(username=username).first():
            session.close()
            return jsonify({'error': 'User already exists'}), 400
        user = User(username=username, password=password, role=role)
        session.add(user)
        session.commit()
        result = {'id': user.id, 'username': user.username, 'role': user.role}
        session.close()
        return jsonify(result), 201

    role_filter = request.args.get('role')
    query = session.query(User)
    if role_filter:
        query = query.filter(User.role == role_filter)
    users = query.all()
    result = [{'id': u.id, 'username': u.username, 'role': u.role} for u in users]
    session.close()
    return jsonify(result)
