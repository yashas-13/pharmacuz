f2igg8-codex/modify-get_user_from_token-to-return-username-and-role
import os
 main
from flask import Flask, jsonify, send_from_directory

from auth import auth_bp
from manufacturer import manufacturer_bp
from cfa import cfa_bp
from super_stockist import super_stockist_bp

app = Flask(__name__, static_folder='../frontend', static_url_path='')

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(manufacturer_bp, url_prefix='/manufacturer')
app.register_blueprint(cfa_bp, url_prefix='/cfa')
app.register_blueprint(super_stockist_bp, url_prefix='/super_stockist')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')
 f2igg8-codex/modify-get_user_from_token-to-return-username-and-role




 main
 main
@app.route('/dashboard')
def dashboard_page():
    """Serve the dashboard page for logged in users."""
    return send_from_directory(app.static_folder, 'dashboard.html')
 f2igg8-codex/modify-get_user_from_token-to-return-username-and-role

 main
 main
 main

if __name__ == '__main__':
    # Allow overriding port via the PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)
