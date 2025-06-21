import os
from flask import Flask, send_from_directory
from flask_cors import CORS

from .models import db
from .routes.auth import auth_bp
from .routes.manufacturer import manufacturer_bp
from .routes.cfa import cfa_bp
from .routes.super_stockist import super_stockist_bp


def create_app():
    app = Flask(__name__, static_folder='../frontend', static_url_path='')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///pharmacuz.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    CORS(app)
    db.init_app(app)

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(manufacturer_bp, url_prefix='/api/manufacturer')
    app.register_blueprint(cfa_bp, url_prefix='/api/cfa')
    app.register_blueprint(super_stockist_bp, url_prefix='/api/super_stockist')

    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')

    return app
