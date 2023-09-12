"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint, current_app
from api.models import db, User, TokenBlocked
from api.utils import generate_sitemap, APIException

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_jwt_extended import jwt_required

import smtplib, ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from email.mime.base import MIMEBase
from email import encoders


smtp_address = os.getenv("SMTP_ADDRESS")
smtp_port = os.getenv("SMTP_PORT")
email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")

api = Blueprint('api', __name__)



def send_email(asunto, destinatario, body):
    message = MIMEMultipart("alternative")
    message["Subject"] = asunto
    message["From"] = email_address
    message["To"] = destinatario
    
    #Version HTML del body
    html = ''' 
    
    <html>
    <body>
    <div>
    <h1>
    Hola 
    </h1>
     ''' + body + '''   
    </div>
    </body>
    </html>
    '''

    #crear los elemento MIME
    html_mime = MIMEText(html, 'html')

    #adjuntamos el código html al mensaje
    message.attach(html_mime)

    #enviar el correo
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_address, smtp_port, context=context) as server:
            server.login(email_address, email_password)
            server.sendmail(email_address, destinatario, message.as_string())
        return True
    
    except Exception as error:
        print(str(error))
        return False


def verifyToken(jti):
    search = TokenBlocked.query.filter_by(token=jti).first()
    
    if search == None:
        return True #para este caso el token no estaría en la lista de bloqueados
    else:
        return False #para este caso el token sí estaría en la lista de bloqueados



@api.route('/hello', methods=['POST', 'GET'])
@jwt_required()
def handle_hello():

    verification = verifyToken(get_jwt()["jti"])
    if verification == False:
        return jsonify({"message":"forbidden"}), 403 

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

@api.route("/login", methods=["POST"])
def login():
    body = request.get_json()
    email = body["email"]
    password = body["password"]

    if body is None:
        raise APIException("Body está vacío", status_code=400)
    if email is None or email=="":
        raise APIException("El email es necesario", status_code=400)
    if password is None or password=="":
        raise APIException("El password es necesario", status_code=400)
    
    user = User.query.filter_by(email=email).first()
    if user is None:
        raise APIException("El usuario o el password son incorrectos", status_code=400)
   
    coincidencia = current_app.bcrypt.check_password_hash(user.password,password) #si coincide, devuelve True

    if not coincidencia:
        raise APIException("El usuario o el password son incorrectos", status_code=400)
    
    access_token = create_access_token(identity=email)
    return jsonify({"token":access_token, "message":"login correcto"}), 200


@api.route("/sendmail", methods=["POST"])
def endpoint_mail():
    body = request.get_json()
    asunto = body["asunto"]
    destinatario = body["destinatario"]
    cuerpo = body["contenido"]

    verificar = send_email(asunto, destinatario, cuerpo)

    if verificar==True:
        return jsonify({"message":"email sent"}), 200
    else:
        return jsonify({"message":"error sending mail"}), 400


@api.route('/user/upload-image', methods=['PUT'])
@jwt_required()
def handle_upload():

    # validate that the front-end request was built correctly
    if 'profile_image' in request.files:
        #print("request.files: ", request.files)
        #print("request.form.info: ", request.form["info"])

        # upload file to uploadcare
        result = current_app.cloudinary.uploader.upload(request.files['profile_image'])
        #print(result)
        #obtain user identity
        identity = get_jwt_identity()
        #print(identity)

        # fetch for the user
        user1 = User.query.filter_by(email=identity).first()

        # update the user with the given cloudinary image URL
        user1.profile_image_url = result['secure_url']

        db.session.add(user1)
        db.session.commit()

        return jsonify(user1.serialize()), 200
    else:
        raise APIException('Missing profile_image on the FormData')


@api.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    try:
        jti = get_jwt()["jti"]
        identity = get_jwt_identity() #asociada al correo
        print("jti: ", jti)
        new_register =  TokenBlocked(token=jti, email= identity) #creamos una instancia de la clase TokenBlocked

        db.session.add(new_register)
        db.session.commit()

        return jsonify({"message":"logout succesfully"}), 200
    
    except Exception as error:
        print(str(error))
        return jsonify({"message":"error trying to logout"}), 403


