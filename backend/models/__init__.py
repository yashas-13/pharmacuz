from sqlalchemy.orm import declarative_base

Base = declarative_base()
from .audit_log import AuditLog

