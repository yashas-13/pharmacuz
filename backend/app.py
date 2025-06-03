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

if __name__ == '__main__':
    app.run(debug=True)
