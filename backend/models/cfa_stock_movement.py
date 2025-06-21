from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from . import Base

class CFAStockMovement(Base):
    __tablename__ = 'cfa_stock_movements'
    id = Column(Integer, primary_key=True)
    cfa = Column(String, nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    batch_no = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    action = Column(String, nullable=False)  # received or dispatched
    timestamp = Column(DateTime, default=datetime.utcnow)
