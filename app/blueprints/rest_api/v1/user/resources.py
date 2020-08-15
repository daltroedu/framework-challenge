from datetime import timedelta

from flask import abort, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from app.blueprints.models import User
from app.blueprints.rest_api.utils import error_response
from app.blueprints.rest_api.v1 import rest_api_v1
from app.blueprints.rest_api.v1.user.serializers import user_schema, users_schema
from app.ext.database.flask_sqlalchemy import db


@rest_api_v1.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}

    email = data['email']
    username = data['username']
    
    if User.query.filter_by(email=email).first():
        return error_response(409, 'please use a different email')

    if User.query.filter_by(username=username).first():
        return error_response(409, 'please use a different username')

    password = generate_password_hash(data['password'])
    name = data['name']
    user = User(email, username, password, name)

    try:
        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user)
        return jsonify(result), 201
    except BaseException as e:
        db.session().rollback()
        return jsonify({'message': 'unable to create'}), 500


@rest_api_v1.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}

    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return error_response(404, 'email not found')

    if not check_password_hash(user.password, data['password']):
        return error_response(401, 'incorrect password')

    access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
    return jsonify({'access_token': access_token}), 201