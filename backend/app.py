import os
from flask import Flask, send_from_directory

from backend.auth import auth_bp
from backend.routes.manufacturer import manufacturer_bp
from backend.routes.cfa import cfa_bp
from backend.routes.super_stockist import super_stockist_bp
from backend.routes.order import order_bp
from backend.routes.product import product_bp
from backend.routes.inventory import inventory_bp
from backend.routes.audit import audit_bp
from backend.routes.sync import sync_bp
from backend.routes.pricing import pricing_bp
from backend.routes.recall import recall_bp
from backend.routes.pack_config import pack_config_bp
from backend.routes.cfa_stock import cfa_stock_bp
from backend.routes.analytics import analytics_bp
from backend.routes.offer import offer_bp
from backend.database import engine, SessionLocal
from backend.models import Base
from backend.models.order import Order  # ensure table registration
from backend.models.batch import Batch
from backend.models.pack_config import PackConfig
from backend.models.product import Product
from backend.models.user import User
from backend.models.inventory import Inventory
from backend.models.pricing_catalog import PricingCatalog
from backend.models.audit_log import AuditLog
from backend.models.recall import Recall
from backend.models.cfa_stock_movement import CFAStockMovement
from backend.models.offer import Offer

app = Flask(__name__, static_folder="../frontend", static_url_path="")

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)


# Seed sample products if table is empty
def seed_products():
    session = SessionLocal()
    if session.query(Product).count() == 0:
        samples = [
            {
                "name": "PANSZ-DSR",
                "description": "Pantoprazole 40mg + Domperidone 30mg SR (Capsules)",
            },
            {
                "name": "XIMPRAZ",
                "description": "Esomeprazole 40mg + Domperidone 30mg SR (Capsules)",
            },
            {
                "name": "SOOKRAL SUSP",
                "description": "Sucralfate 500mg + Oxetacaine 10mg Suspension (100ml)",
            },
            {
                "name": "ZEKMOL 250 SUSP",
                "description": "Paracetamol 250mg Suspension (60ml)",
            },
            {
                "name": "ZOACE-P",
                "description": "Aceclofenac 100mg + Paracetamol 325mg (Tablet)",
            },
            {
                "name": "ZOACE-SP",
                "description": "Aceclofenac + Paracetamol + Serratiopeptidase (Tablet)",
            },
            {
                "name": "CAVIZIC",
                "description": "Calcium Citrate + Magnesium + Vitamin K2 + D3 etc.",
            },
            {"name": "ZIFLOZIN", "description": "Dapagliflozin 10mg (Tablet)"},
        ]
        for p in samples:
            session.add(Product(name=p["name"], description=p["description"]))
        session.commit()
    session.close()


seed_products()

# Register blueprints under /api prefix
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(manufacturer_bp, url_prefix="/api/manufacturer")
app.register_blueprint(cfa_bp, url_prefix="/api/cfa")
app.register_blueprint(super_stockist_bp, url_prefix="/api/super_stockist")
app.register_blueprint(order_bp, url_prefix="/api")
app.register_blueprint(product_bp, url_prefix="/api")
app.register_blueprint(inventory_bp, url_prefix="/api")
app.register_blueprint(audit_bp, url_prefix="/api")
app.register_blueprint(sync_bp, url_prefix="/api")
app.register_blueprint(pricing_bp, url_prefix="/api")
app.register_blueprint(recall_bp, url_prefix="/api")
app.register_blueprint(pack_config_bp, url_prefix="/api")
app.register_blueprint(cfa_stock_bp, url_prefix="/api")
app.register_blueprint(analytics_bp, url_prefix="/api")
app.register_blueprint(offer_bp, url_prefix="/api")


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 0))
    app.run(debug=True, port=port)
