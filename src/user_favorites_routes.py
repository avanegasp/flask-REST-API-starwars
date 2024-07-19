import os
from flask import Blueprint, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, PlanetFavorite, Planet

user_fav_bp = Blueprint('favorite_user_routes', __name__)

@user_fav_bp.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_all_user_favorites(user_id):
    try:
        planets_favorites_user = PlanetFavorite.query.filter_by(user_id=user_id).all()
        planets_details = [Planet.query.get(fav.planet_id).serialize() for fav in planets_favorites_user]

        response = {
            "planets_favorites":planets_details
        }
        return jsonify(response), 200
    
    except Exception as error:
        return jsonify({"error", f"{error}" }), 500