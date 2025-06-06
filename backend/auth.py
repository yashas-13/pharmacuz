from flask import Blueprint, request, jsonify
import uuid

auth_bp = Blueprint('auth', __name__)

# Simple in-memory user store
USERS = {
    'admin': {'password': 'adminpass', 'role': 'manufacturer'},
    'cfauser': {'password': 'cfapass', 'role': 'cfa'},
    'stockist': {'password': 'stockpass', 'role': 'super_stockist'},
}

# Token store mapping token to username
TOKENS = {}

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    username = data.get('username')
    password = data.get('password')
    user = USERS.get(username)
    if not user or user['password'] != password:
        return jsonify({'error': 'Invalid credentials'}), 401
    token = str(uuid.uuid4())
    TOKENS[token] = username
    return jsonify({'token': token, 'role': user['role']})


def get_user_from_token(token):
    """Return username and role for a valid token.

    The password field is intentionally omitted to avoid exposing
    credentials. ``None`` is returned for invalid tokens or unknown users.
    """
    username = TOKENS.get(token)
    if not username:
        return None
    user = USERS.get(username)
    if not user:
        return None
    return {
        'username': username,
        'role': user['role']
    }


def role_required(role):
    def decorator(func):
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({'error': 'Missing token'}), 401
            token = auth_header.split(' ')[1]
            user = get_user_from_token(token)
            if not user:
                return jsonify({'error': 'Invalid token'}), 401
            if user['role'] != role:
                return jsonify({'error': 'Forbidden'}), 403
            request.user = user
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator
