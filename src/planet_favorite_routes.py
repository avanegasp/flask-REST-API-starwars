import os
from flask import Blueprint, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, PlanetFavorite

planet_fav_bp = Blueprint('planet_favorite_route', __name__)

#CRUD PLANET_FAVORITE

@planet_fav_bp.route('/planetfavorites', methods=['GET'])
def get_all_planet_favorites():
    try:
        planet_favorites = PlanetFavorite.query.all()
        if not planet_favorites:
            return jsonify({"error":"No planet_favorites found"}), 400
        serialized_planet_favorites = [planet_favorite.serialize() for planet_favorite in planet_favorites]
        return jsonify({"planet_favorite":serialized_planet_favorites}), 200
    except Exception as error:
        return jsonify({"error", str(error)}),400
    
@planet_fav_bp.route('/planetfavorite/<int:user_id>/<int:planet_id>', methods=['POST'])
def get_favorite_planet(user_id, planet_id):

    body = request.json

    user_id = body.get("user_id", None)
    planet_id = body.get("planet_id", None)

    if user_id is None or planet_id is None:
        return jsonify({"error", "Missing values"}), 400
    
    planet_favorite_user_exist = PlanetFavorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if planet_favorite_user_exist is not None:
        return jsonify({"error": f"planet {planet_id} and user {user_id} already exists"}),400

    planet_favorites = PlanetFavorite(user_id=user_id, planet_id=planet_id)

    try:
        db.session.add(planet_favorites)
        db.session.commit()
        db.session.refresh(planet_favorites)

        return jsonify({"message": f"planet_favorite {planet_id} with user {user_id} created successfully!"}), 201
    except Exception as error:
        return jsonify({"error": f"{error}"}),500
