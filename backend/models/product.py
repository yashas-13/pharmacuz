from sqlalchemy import Column, Integer, String
from . import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    hsn = Column(String, nullable=True)
    gst = Column(String, nullable=True)
    composition = Column(String, nullable=True)
    category = Column(String, nullable=True)
