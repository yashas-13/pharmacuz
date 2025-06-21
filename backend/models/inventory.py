from sqlalchemy import Column, Integer, String, Date, ForeignKey
from . import Base

class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    location = Column(String, nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    batch_no = Column(String, nullable=False)
    exp_date = Column(Date, nullable=True)
    quantity = Column(Integer, nullable=False)
