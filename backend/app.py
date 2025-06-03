from flask import Flask, jsonify

from auth import auth_bp
from manufacturer import manufacturer_bp
from cfa import cfa_bp
from super_stockist import super_stockist_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(manufacturer_bp, url_prefix='/manufacturer')
app.register_blueprint(cfa_bp, url_prefix='/cfa')
app.register_blueprint(super_stockist_bp, url_prefix='/super_stockist')

@app.route('/')
def index():
    return jsonify({'message': 'Pharmacuz API'})

if __name__ == '__main__':
    app.run(debug=True)
