"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint, current_app
from api.models import db, User
from api.utils import generate_sitemap, APIException

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

#current_app.bcrypt
#current_app.jwt

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/signup', methods=["POST"])
def user_register():
    body = request.get_json()
    email = body["email"]
    password = body["password"]
    is_active = True

    if body is None:
        raise APIException("Body está vacío", status_code=400)
    if email is None or email=="":
        raise APIException("El email es necesario", status_code=400)
    if password is None or password=="":
        raise APIException("El password es necesario", status_code=400)
    
    user = User.query.filter_by(email=email).first()

    #se verifica si el usuario ya existe en BD
    if user:
        raise APIException("El usario ya existe", status_code=400)

    #debería encriptar el password
    print("password sin encriptar:", password)
    password = current_app.bcrypt.generate_password_hash(password, 10).decode("utf-8")
    print("password con encriptación:", password)

    new_register = User(email=email,
                        password=password,
                        is_active= is_active)
    try: 
        db.session.add(new_register)
        db.session.commit()
        return jsonify({"message":"Usuario registrado"}), 201
    except Exception as error:
        print(str(error))
        return jsonify({"message":"error al almacenar en BD"}), 500
