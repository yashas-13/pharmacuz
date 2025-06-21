from sqlalchemy import Column, Integer, String
from . import Base

class GRN(Base):
    __tablename__ = 'grns'
    id = Column(Integer, primary_key=True)
    batch = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
