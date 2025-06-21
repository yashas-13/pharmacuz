from datetime import date
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from backend.auth import roles_required, role_required
from backend.database import SessionLocal
from backend.models.offer import Offer
from backend.models.product import Product

offer_bp = Blueprint('offer', __name__)


def _parse_date(value):
    if isinstance(value, str) and value:
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None
    return value


@offer_bp.route('/offers', methods=['GET', 'POST'])
@roles_required('manufacturer', 'cfa', 'super_stockist')
def offers():
    session: Session = SessionLocal()
    if request.method == 'POST':
        if request.user['role'] != 'manufacturer':
            session.close()
            return jsonify({'error': 'Forbidden'}), 403
        data = request.json or {}
        product_id = data.get('product_id')
        start_date = _parse_date(data.get('start_date'))
        end_date = _parse_date(data.get('end_date'))
        if not product_id or not start_date or not end_date:
            session.close()
            return jsonify({'error': 'Invalid offer data'}), 400
        offer = Offer(
            product_id=product_id,
            description=data.get('description'),
            discount=data.get('discount', 0.0),
            start_date=start_date,
            end_date=end_date,
            active=1,
        )
        session.add(offer)
        session.commit()
        result = {
            'id': offer.id,
            'product_id': offer.product_id,
            'description': offer.description,
            'discount': offer.discount,
            'start_date': str(offer.start_date),
            'end_date': str(offer.end_date),
            'active': offer.active,
        }
        session.close()
        return jsonify(result), 201

    # GET
    active_only = request.args.get('active')
    query = session.query(Offer)
    if active_only == '1':
        today = date.today()
        query = query.filter(Offer.start_date <= today, Offer.end_date >= today, Offer.active == 1)
    offers = query.all()
    result = [
        {
            'id': o.id,
            'product_id': o.product_id,
            'description': o.description,
            'discount': o.discount,
            'start_date': str(o.start_date),
            'end_date': str(o.end_date),
            'active': o.active,
        }
        for o in offers
    ]
    session.close()
    return jsonify(result)


@offer_bp.route('/offers/<int:offer_id>', methods=['PUT', 'DELETE'])
@role_required('manufacturer')
def manage_offer(offer_id: int):
    session: Session = SessionLocal()
    offer = session.query(Offer).get(offer_id)
    if not offer:
        session.close()
        return jsonify({'error': 'Offer not found'}), 404
    if request.method == 'DELETE':
        session.delete(offer)
        session.commit()
        session.close()
        return jsonify({'message': 'deleted'})
    data = request.json or {}
    if 'product_id' in data:
        offer.product_id = data['product_id']
    if 'description' in data:
        offer.description = data['description']
    if 'discount' in data:
        offer.discount = data['discount']
    if 'start_date' in data:
        offer.start_date = _parse_date(data['start_date'])
    if 'end_date' in data:
        offer.end_date = _parse_date(data['end_date'])
    if 'active' in data:
        offer.active = data['active']
    session.commit()
    result = {
        'id': offer.id,
        'product_id': offer.product_id,
        'description': offer.description,
        'discount': offer.discount,
        'start_date': str(offer.start_date),
        'end_date': str(offer.end_date),
        'active': offer.active,
    }
    session.close()
    return jsonify(result)
