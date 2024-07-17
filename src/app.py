"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Gender, Character

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#CRUD users

@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = User.query.all()
        if not users:
            return jsonify({"error": "No users found"}), 400
        serialized_users = [user.serialize() for user in users]
        return jsonify({"users": serialized_users}), 200
    except Exception as error:
        return jsonify({"error":str(error)}), 400

@app.route('/user', methods=['POST'])
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



#CRUD characters

@app.route('/characters', methods=['GET'])
def get_all_characters():
    try:
        characters = Character.query.all()
        if not characters:
            return jsonify({"error":"No characters found"}), 400
        serialized_characters = [character.serialize() for character in characters]
        return jsonify({"characters": serialized_characters }), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 400


@app.route('/character', methods=['POST'])
def character_create():
    body = request.json

    character_name = body.get("character_name", None)
    character_gender = body.get("character_gender", None)
    hair_color = body.get("hair_color", None)
    eyes_color = body.get("eyes_color", None)

    required_fields = ["character_name", "character_gender", "hair_color", "eyes_color"]

    for field in required_fields:
        if field not in body:
            return jsonify({"error": f"Missing field '{field}'"}),400

    character = Character(character_name=character_name, character_gender=character_gender, hair_color=hair_color, eyes_color=eyes_color)

    try:
        db.session.add(character)
        db.session.commit()
        db.session.refresh(character)

        return jsonify({"message": f"Character {character.character_name} created successfully"}), 201

    except Exception as error:
        return jsonify({"error": f"{error}"}), 500
    

@app.route('/character/<int:character_id>', methods=['GET'])
def get_character(character_id):

    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"error": "Character not found"}), 404
    
    return jsonify({
        "message": f"character: {character} founded successfully"
    })










# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
