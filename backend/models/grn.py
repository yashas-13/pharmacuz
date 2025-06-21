from . import db

class GRN(db.Model):
    __tablename__ = 'grns'
    id = db.Column(db.Integer, primary_key=True)
    batch = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
