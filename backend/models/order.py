from sqlalchemy import Column, Integer, String, Date
from datetime import date
from . import Base

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    product = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default='created')
    placed_by = Column(String, nullable=True)
    target = Column(String, nullable=True)
    batch_no = Column(String, nullable=True)
    mfg_date = Column(Date, nullable=True)
    exp_date = Column(Date, nullable=True)
    order_date = Column(Date, default=date.today)
