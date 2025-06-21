from sqlalchemy import Column, Integer, String, ForeignKey
from . import Base

class PackConfig(Base):
    __tablename__ = 'pack_configs'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    pack_type = Column(String, nullable=False)
    units_per_pack = Column(String, nullable=True)
    dimensions = Column(String, nullable=True)
