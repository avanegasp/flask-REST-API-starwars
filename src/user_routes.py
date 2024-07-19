import os
from flask import Blueprint, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Gender, PlanetFavorite, Planet

user_bp = Blueprint('user_routes', __name__)

#CRUD users

@user_bp.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = User.query.all()
        if not users:
            return jsonify({"error": "No users found"}), 400
        serialized_users = [user.serialize() for user in users]
        return jsonify({"users": serialized_users}), 200
    except Exception as error:
        return jsonify({"error":str(error)}), 400

@user_bp.route('/user', methods=['POST'])
def create_user():
    body = request.json

    name = body.get("name", None)
    last_name = body.get("last_name", None)
    gender = body.get("gender", None)
    email = body.get("email", None)
    suscription_date = body.get("suscription_date", None)

    required_fields = ["name", "last_name", "gender", "email", "suscription_date"]

    for field in required_fields:
        if field not in body:
            return jsonify({"error": f"Missing field '{field}'"}),400

    user = User(name=name, last_name=last_name, gender=Gender(gender), email=email, suscription_date=suscription_date)

    try:
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)

        return jsonify({"message": f"User {user.name} created successfully!"}),201
    
    except Exception as error:
        return jsonify({"error": f"{error}"}), 500
    

@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if user is None:
            return jsonify({"error": "user not found!"}), 404
        return jsonify({"user": user.serialize()}), 200
    except Exception as error:
        return jsonify({"error", f"Missing field {error}"})


