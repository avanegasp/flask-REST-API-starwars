import os
from flask import Blueprint, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, CharacterFavorite

character_fav_bp = Blueprint('character_favorites_routes', __name__)

@character_fav_bp.route('/character_favorites', methods=['GET'])
def get_all_character_favorites():
    try:
        character_favorites = CharacterFavorite.query.all()
        if not character_favorites:
            return jsonify({"error": "No character_favorites found"}), 400
        serialized_character_favorites = [character_favorites.serialize() for character_favorites in character_favorites]
        return jsonify({"character_favorite": serialized_character_favorites}),200

    except Exception as error:
        return jsonify({"error": str({error})}), 400
    
@character_fav_bp.route('/character_favorite/<user_id>/<character_id>', methods=['POST'])
def create_character_favorite_to_user(user_id,character_id):
    body = request.json

    user_id = body.get("user_id",None)
    character_id = body.get("character_id", None)

    if user_id is None or character_id is None:
        return jsonify({"error": "Missing values"}),400
    
    character_favorite_user_exist = CharacterFavorite.query.filter_by(user_id=user_id, character_id=character_id).first()
    if character_favorite_user_exist is not None:
        return jsonify({"error": f"character {character_id} and user {user_id} already exist"}), 400
    
    character_favorites = CharacterFavorite(user_id=user_id, character_id=character_id)

    try:
        db.session.add(character_favorites)
        db.session.commit()
        db.session.refresh(character_favorites)

        return jsonify({"message": f"character_favorite {character_id} with user {user_id} created successfully!"}),201

    except Exception as error:
        return jsonify({"error": f"{error}"}),500

@character_fav_bp.route('/character_favorite/<character_id>', methods=['DELETE'])
def character_fav_deleted(character_id):
    try:
        character_favorites = CharacterFavorite.query.filter_by(character_id=character_id).all()
        if character_favorites is None:
            return jsonify({"error":"character_fav not found"}),404
        
        for fav in character_favorites:
            db.session.delete(fav)
        db.session.commit()

        return jsonify({"message": f"character_fav with id {character_id} is deleted"}),200

    except Exception as error:
        db.session.rollback()
        return jsonify({"error": f"{error}"}),500