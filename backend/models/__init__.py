from sqlalchemy.orm import declarative_base

Base = declarative_base()
from .audit_log import AuditLog
from .pricing_catalog import PricingCatalog
from .recall import Recall
from .cfa_stock_movement import CFAStockMovement
from .offer import Offer

