from backend.app import app

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, port=port)
