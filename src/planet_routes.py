import os
from flask import Blueprint, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Planet

planet_bp = Blueprint('planet_routes', __name__)

#CRUD Planets

@planet_bp.route('/planets', methods=['GET'])
def get_all_planets():
    try:
        planets = Planet.query.all()
        if not planets:
            return jsonify({"error":"No planets found"}), 400
        serialized_planets = [planet.serialize() for planet in planets]
        return jsonify({"planets":serialized_planets}), 200
    except Exception as error:
        return jsonify({"error", str(error)}),400


@planet_bp.route('/planet', methods=['POST'])
def create_planet():

    body = request.json

    name = body.get("name", None)
    population = body.get("population", None)
    terrain = body.get("terrain", None)
    surface_water = body.get("surface_water", None)
    gravity = body.get("gravity", None)

    required_fields = ["name", "population", "terrain", "surface_water", "gravity"]

    for field in required_fields:
        if field not in body:
            return jsonify({"error": f"Missiong field {field}"}),400
        
    planet = Planet(name=name, population=population, terrain=terrain, surface_water=surface_water, gravity=gravity)

    try:
        db.session.add(planet)
        db.session.commit()
        db.session.refresh(planet)

        return jsonify({"message": f"Planet {planet.name} created successfully"})

    except Exception as error:
        return jsonify({"error": f"{error}"}), 500

@planet_bp.route('/planet/<int:id>', methods=['GET'])
def get_planet(id):
    
    planet = Planet.query.get(id)
    if planet is None:
        return jsonify({"error":"Planet not found"}), 404
    
    return jsonify({
        "message": f"Planet:{planet} founded successfully"
    })

@planet_bp.route('/planet/<int:id>', methods=['PUT'])
def update_planet(id):
    body = request.json

    planet = Planet.query.get(id)
    if planet is None:
        return jsonify({"error": "Planet not found"}),404
    
    required_fields = ["name", "population", "terrain", "surface_water", "gravity"]

    missing_fields = [field for field in required_fields if field not in body]
    if missing_fields:
        return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}),400
    
    name = body.get("name")
    population = body.get("population")
    terrain = body.get("terrain")
    surface_water = body.get("surface_water")
    gravity = body.get("gravity")

    planet.name = name
    planet.population = population
    planet.terrain = terrain
    planet.surface_water = surface_water
    planet.gravity = gravity

    try:
        db.session.commit()
        return jsonify({"planet":planet.serialize()}),200

    except Exception as error:
        db.session.rollback()
        return jsonify({"error": str(error)}),500


@planet_bp.route('/planet/<int:id>', methods=['DELETE'])
def deleted_planet(id):
    try:
        planet = Planet.query.get(id)
        if planet is None:
            return jsonify({"error":"planet not found"}),404
        db.session.delete(planet)
        db.session.commit()

        return jsonify({"message":f"planet with id {id} deleted"}),200

    except Exception as error:
        db.session.rollback()
        return jsonify({"error": f"{error}"}),500
    
