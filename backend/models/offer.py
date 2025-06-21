from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from . import Base

class Offer(Base):
    __tablename__ = 'offers'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    description = Column(String, nullable=True)
    discount = Column(Float, default=0.0)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    active = Column(Integer, default=1)  # 1=true,0=false
