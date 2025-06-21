import os
from flask import Flask, send_from_directory

from backend.auth import auth_bp
from backend.routes.manufacturer import manufacturer_bp
from backend.routes.cfa import cfa_bp
from backend.routes.super_stockist import super_stockist_bp
from backend.routes.order import order_bp
from backend.database import engine
from backend.models import Base
from backend.models.order import Order  # ensure table registration
from backend.models.batch import Batch
from backend.models.pack_config import PackConfig
from backend.models.user import User

app = Flask(__name__, static_folder='../frontend', static_url_path='')

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Register blueprints under /api prefix
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(manufacturer_bp, url_prefix='/api/manufacturer')
app.register_blueprint(cfa_bp, url_prefix='/api/cfa')
app.register_blueprint(super_stockist_bp, url_prefix='/api/super_stockist')
app.register_blueprint(order_bp, url_prefix='/api')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, port=port)
