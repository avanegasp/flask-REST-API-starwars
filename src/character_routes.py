import os
from flask import Blueprint, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Character

character_bp = Blueprint('character_routes', __name__)

#CRUD characters

@character_bp.route('/characters', methods=['GET'])
def get_all_characters():
    try:
        characters = Character.query.all()
        if not characters:
            return jsonify({"error":"No characters found"}), 400
        serialized_characters = [character.serialize() for character in characters]
        return jsonify({"characters": serialized_characters }), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 400


@character_bp.route('/character', methods=['POST'])
def create_character():
    body = request.json

    name = body.get("name", None)
    gender = body.get("gender", None)
    hair_color = body.get("hair_color", None)
    eyes_color = body.get("eyes_color", None)

    required_fields = ["name", "gender", "hair_color", "eyes_color"]

    for field in required_fields:
        if field not in body:
            return jsonify({"error": f"Missing field '{field}'"}),400

    character = Character(name=name, gender=gender, hair_color=hair_color, eyes_color=eyes_color)

    try:
        db.session.add(character)
        db.session.commit()
        db.session.refresh(character)

        return jsonify({"message": f"Character {character.name} created successfully"}), 201

    except Exception as error:
        return jsonify({"error": f"{error}"}), 500
    
    
@character_bp.route('/character/<int:id>', methods=['GET'])
def get_character(id):

    character = Character.query.get(id)
    if character is None:
        return jsonify({"error": "Character not found"}), 404
    
    return jsonify({
        "message": f"Character: {character} founded successfully"
    })

@character_bp.route('/character/<int:id>', methods=['PUT'])
def update_character(id):
    body = request.json

    character = Character.query.get(id)
    if character is None:
        return jsonify({"error": "Character not found"}),404
    
    required_fields = ["name", "gender", "hair_color", "eyes_color"]

    missing_fields = [field for field in required_fields if field not in body]
    if missing_fields:
        return jsonify({"error":f"Missing fields:{', '.join(missing_fields)}"}),400
    
    name = body.get("name",None)
    gender = body.get("gender",None)
    hair_color = body.get("hair_color",None)
    eyes_color = body.get("eyes_color",None)

    character.name = name
    character.gender = gender
    character.hair_color = hair_color
    character.eyes_color = eyes_color

    try:
        db.session.commit()
        return jsonify({"character":character.serialize()})
    
    except Exception as error:
        db.session.rollback()
        return jsonify({"error": str(error)}),500



@character_bp.route('/character/<int:id>', methods=['DELETE'])
def deleted_character(id):
    try:
        character = Character.query.get(id)
        if character is None:
            return jsonify({"error":"character not found"}),404
        db.session.delete(character)
        db.session.commit()

        return jsonify({"message":f"character with id {id} deleted"}),200    

    except Exception as error:
        db.session.rollback()
        return jsonify({"error": f"{error}"}),500