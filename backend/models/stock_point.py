from sqlalchemy import Column, Integer, String, ForeignKey
from . import Base

class StockPoint(Base):
    __tablename__ = 'stock_points'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cfa_username = Column(String, ForeignKey('users.username'), nullable=False)
    active = Column(Integer, default=1)
