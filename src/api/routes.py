"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Profile, Post
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select


api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/register', methods=["POST"])
def register():
    body = request.get_json()

    if not body["email"] and not body["password"]:
        return jsonify({"msg": "missing info"}), 403  

    user = db.session.execute(select(User).where(User.email == body["email"])).scalar_one_or_none()
    if user:
        return jsonify({"msg": "email taken"}), 403  


    hashed = generate_password_hash(body["password"])

    new_user = User(
        email= body["email"],
        password=hashed,
        is_active=True
        )
    db.session.add(new_user)
    db.session.flush() #le asigna un el id al usuario, NO HA ALMACENADO NADA

    #y el perfil??? 
    new_profile = Profile(
        bio='describete',
        user_id= new_user.id
    )
    db.session.add(new_profile)
    db.session.commit()

    token = create_access_token(identity=str(new_user.id))
    
    return jsonify({"msg": "created", "user": new_user.serialize(), "token": token}), 201



@api.route('/login', methods=["POST"])
def login():
    body = request.get_json()

    if not body["email"] and not body["password"]:
        return jsonify({"msg": "missing info"}), 403  

    user = db.session.execute(select(User).where(User.email == body["email"])).scalar_one_or_none()
    if not user:
        return jsonify({"msg": "email not found"}), 404  

    #comparar password
    if not check_password_hash(user.password, body["password"]):
        return jsonify({"msg": "email/password wrong"}), 401  
    
    token = create_access_token(identity=str(user.id))
    
    return jsonify({"msg": "logged", "user": user.serialize(), "token": token}), 200

#todo post, put, delete y get con info privada va con jwt_required
@api.route('/post', methods=["POST"])
@jwt_required() #--> si no se envia el token, NO PASA --> ES GANDALF
def create_post():
    id = get_jwt_identity() #extraigo del token el identity que pusimos al crear token (user.id)
    body = request.get_json()

    new_post = Post(
        title= body["title"],
        user_id = id
    )
    db.session.add(new_post)
    db.session.commit()

    return jsonify({"created": True}), 201

#todo post, put, delete y get con info privada va con jwt_required
@api.route('/me', methods=["GET"])
@jwt_required() #--> si no se envia el token, NO PASA --> ES GANDALF
def get_me():
    id = get_jwt_identity() #extraigo del token el identity que pusimos al crear token (user.id)
    user = db.session.get(User, id)

    return jsonify({"user": user.serialize()}), 200

