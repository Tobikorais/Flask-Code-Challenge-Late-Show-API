from flask import Blueprint, request, jsonify
from ..models.user import User
from ..app import db
from flask_jwt_extended import create_access_token
from datetime import datetime
from ..middleware import validate_json, validate_schema, sanitize_input

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
@validate_json
@validate_schema({'username': str, 'password': str})
@sanitize_input
def register():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']

        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 409

        try:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return jsonify({
                'message': 'User registered successfully',
                'user': {'id': user.id, 'username': user.username}
            }), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/login', methods=['POST'])
@validate_json
@validate_schema({'username': str, 'password': str})
@sanitize_input
def login():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            if not user.is_active:
                return jsonify({'error': 'Account is deactivated'}), 403

            access_token = create_access_token(identity=user.id)
            user.last_login = datetime.utcnow()
            db.session.commit()

            return jsonify({
                'access_token': access_token,
                'user': {'id': user.id, 'username': user.username}
            }), 200
        return jsonify({'error': 'Invalid username or password'}), 401

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500 