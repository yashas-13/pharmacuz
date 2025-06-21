from sqlalchemy import Column, Integer, String
from . import Base

class StockRequest(Base):
    __tablename__ = 'stock_requests'
    id = Column(Integer, primary_key=True)
    product = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
