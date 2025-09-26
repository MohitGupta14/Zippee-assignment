from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from ..extensions import db, blacklisted_tokens
from ..models import User
from datetime import timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# ------------------------
# Register new user
# ------------------------
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}

    # Check required fields
    if not all(field in data for field in ['username', 'email', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400

    # Check if username/email already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400

    # Create user
    user = User(
        username=data['username'],
        email=data['email'],
        role=data.get('role', 'user')  # Default role: user
    )
    user.set_password(data['password'])

    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created', 'user': user.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create user'}), 500

# ------------------------
# Login
# ------------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}

    if not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Username and password required'}), 400

    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({'access_token': access_token, 'user': user.to_dict()}), 200

    return jsonify({'error': 'Invalid credentials'}), 401

# ------------------------
# Logout
# ------------------------
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    blacklisted_tokens.add(jti)
    return jsonify({'message': 'Logged out successfully'}), 200
