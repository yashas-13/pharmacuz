from sqlalchemy import Column, Integer, String, Date
from . import Base

class Recall(Base):
    __tablename__ = 'recalls'
    id = Column(Integer, primary_key=True)
    batch_no = Column(String, nullable=False)
    reason = Column(String, nullable=False)
    start_date = Column(Date, nullable=False)
    status = Column(String, default='active')
