from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from . import Base

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True)
    event_type = Column(String, nullable=False)
    details = Column(String, nullable=False)
    username = Column(String, nullable=True)
    role = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

