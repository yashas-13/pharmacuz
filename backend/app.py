#dqdva9-codex/summarize-pharmacuz-project-overview
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
=======
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage for demonstration purposes
PRODUCTS = []
BATCHES = []

@app.route('/')
def index():
    return jsonify({"message": "Pharmacuz API"})

@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        data = request.json
        if not data or 'name' not in data:
            return jsonify({'error': 'Invalid product data'}), 400
        product = {
            'id': len(PRODUCTS) + 1,
            'name': data['name'],
        }
        PRODUCTS.append(product)
        return jsonify(product), 201
    return jsonify(PRODUCTS)

@app.route('/batches', methods=['GET', 'POST'])
def batches():
    if request.method == 'POST':
        data = request.json
        if not data or 'product_id' not in data or 'quantity' not in data:
            return jsonify({'error': 'Invalid batch data'}), 400
        batch = {
            'id': len(BATCHES) + 1,
            'product_id': data['product_id'],
            'quantity': data['quantity'],
        }
        BATCHES.append(batch)
        return jsonify(batch), 201
    return jsonify(BATCHES)
 main

if __name__ == '__main__':
    app.run(debug=True)
