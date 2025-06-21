from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from . import Base

class PricingCatalog(Base):
    __tablename__ = 'pricing_catalog'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    region = Column(String, nullable=False)
    ptr = Column(Float, nullable=False)
    pts = Column(Float, nullable=False)
    effective_date = Column(Date, nullable=False)
