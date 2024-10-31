"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from src.utils import APIException, generate_sitemap
from admin import setup_admin
from models import db
from user_routes import user_bp
from character_routes import character_bp
from planet_routes import planet_bp
from planet_favorites_routes import planet_fav_bp
from user_favorites_routes import user_fav_bp
from character_favorites_routes import character_fav_bp

#from models import Person

app = Flask(__name__)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(user_fav_bp, url_prefix='/api')
app.register_blueprint(character_bp, url_prefix='/api')
app.register_blueprint(planet_bp, url_prefix='/api')
app.register_blueprint(planet_fav_bp, url_prefix='/api')
app.register_blueprint(character_fav_bp, url_prefix='/api')

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


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
