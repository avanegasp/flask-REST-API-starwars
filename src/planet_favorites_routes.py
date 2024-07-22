import os
from flask import Blueprint, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, PlanetFavorite

planet_fav_bp = Blueprint('planet_favorites_routes', __name__)

#CRUD PLANET_FAVORITE

@planet_fav_bp.route('/planet_favorites', methods=['GET'])
def get_all_planet_favorites():
    try:
        planet_favorites = PlanetFavorite.query.all()
        if not planet_favorites:
            return jsonify({"error":"No planet_favorites found"}), 400
        serialized_planet_favorites = [planet_favorite.serialize() for planet_favorite in planet_favorites]
        return jsonify({"planet_favorite":serialized_planet_favorites}), 200
    except Exception as error:
        return jsonify({"error", str(error)}),400
    
@planet_fav_bp.route('/planet_favorite/<int:user_id>/<int:planet_id>', methods=['POST'])
def create_favorite_planet_to_user(user_id, planet_id):

    body = request.json

    user_id = body.get("user_id", None)
    planet_id = body.get("planet_id", None)

    if user_id is None or planet_id is None:
        return jsonify({"error", "Missing values"}), 400
    
    planet_favorite_user_exist = PlanetFavorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if planet_favorite_user_exist is not None:
        return jsonify({"error": f"planet {planet_id} and user {user_id} already exist"}),400

    planet_favorite = PlanetFavorite(user_id=user_id, planet_id=planet_id)

    try:
        db.session.add(planet_favorite)
        db.session.commit()
        db.session.refresh(planet_favorite)

        return jsonify({"message": f"planet_favorite {planet_id} with user {user_id} created successfully!"}), 201
    except Exception as error:
        return jsonify({"error": f"{error}"}),500

@planet_fav_bp.route("/planet_favorite/<int:planet_id>", methods=["DELETE"])
def planet_fav_deleted(planet_id):
    try:
        planet_favorites = PlanetFavorite.query.filter_by(planet_id=planet_id).all()
        if planet_favorites is None:
            return jsonify({"error": "planet_fav not found"}), 404
        
        for fav in planet_favorites:
            db.session.delete(fav)
        db.session.commit()

        return jsonify({"message":f"planet_fav with id {planet_id} deleted"}),200
        
    except Exception as error:
        db.session.rollback()
        return jsonify({"error": f"{error}"}),500
