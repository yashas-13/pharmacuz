from datetime import datetime
from . import db

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), default='requested')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Product')
