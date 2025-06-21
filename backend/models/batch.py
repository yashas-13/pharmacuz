from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from . import Base

class Batch(Base):
    __tablename__ = 'batches'
    id = Column(Integer, primary_key=True)
    batch_no = Column(String, nullable=False, unique=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    mfg_date = Column(Date, nullable=True)
    exp_date = Column(Date, nullable=True)
    mrp = Column(Float, nullable=True)
    quantity = Column(Integer, nullable=True)
