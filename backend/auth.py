from flask import Blueprint, request, jsonify
import uuid
from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models.user import User

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
    session: Session = SessionLocal()
    user_record = session.query(User).filter_by(username=username).first()
    if user_record:
        if user_record.password != password:
            session.close()
            return jsonify({'error': 'Invalid credentials'}), 401
        role = user_record.role
    else:
        user = USERS.get(username)
        if not user or user['password'] != password:
            session.close()
            return jsonify({'error': 'Invalid credentials'}), 401
        role = user['role']
    token = str(uuid.uuid4())
    TOKENS[token] = username
    session.close()
    return jsonify({'token': token, 'role': role})


def get_user_from_token(token):
    """Return username and role for a valid token.

    The password field is intentionally omitted to avoid exposing
    credentials. ``None`` is returned for invalid tokens or unknown users.
    """
    username = TOKENS.get(token)
    if not username:
        return None
    session: Session = SessionLocal()
    user_record = session.query(User).filter_by(username=username).first()
    if user_record:
        role = user_record.role
    else:
        user = USERS.get(username)
        if not user:
            session.close()
            return None
        role = user['role']
    session.close()
    return {
        'username': username,
        'role': role
    }


def role_required(role):
    """Allow only one specific role."""
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


def roles_required(*roles):
    """Allow any user whose role is in ``roles`` list."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({'error': 'Missing token'}), 401
            token = auth_header.split(' ')[1]
            user = get_user_from_token(token)
            if not user:
                return jsonify({'error': 'Invalid token'}), 401
            if user['role'] not in roles:
                return jsonify({'error': 'Forbidden'}), 403
            request.user = user
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__
        return wrapper
    return decorator
