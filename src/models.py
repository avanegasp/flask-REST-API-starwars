from flask_sqlalchemy import SQLAlchemy
from enum import Enum as SQLEnum


db = SQLAlchemy()

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.id

#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }

class Gender(SQLEnum):
    FEMALE = "Female"
    MALE = "Male"
    OTRO = "Other"    

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.Enum(Gender), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    suscription_date = db.Column(db.Date, nullable=False)

    signIns = db.relationship("SignIn", backref="user")
    planetsFavorites = db.relationship("PlanetFavorite", backref="user")
    charactersFavorites = db.relationship("CharacterFavorite", backref="user")
    starshipsFavorite = db.relationship("StarshipFavorite", backref="user")

class SignIn(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Date, nullable=False)
    success = db.Column(db.Boolean, nullable=False)    

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class Character(db.Model):   

    id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String(100), nullable=False)
    character_gender = db.Column(db.String(50), nullable=False)
    hair_color = db.Column(db.String(50), nullable=False)
    eyes_color = db.Column(db.String(50), nullable=False)

class Planet(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String(100), nullable=False)
    population = db.Column(db.String(100), nullable=False)
    terrain = db.Column(db.String(100), nullable=False)
    surface_water = db.Column(db.String(100), nullable=False)
    gravity = db.Column(db.String(100), nullable=False)

class Starship(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    starship_name = db.Column(db.String, nullable="False")
    model = db.Column(db.String, nullable="False")
    manufacturer = db.Column(db.String, nullable="False")

class CharacterFavorite(db.Model):

    id = db.Column(db.Integer, primary_key=True)
  
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"))

class PlanetFavorite(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))

class StarshipFavorite(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))   
    starship_id = db.Column(db.Integer, db.ForeignKey("starship.id"))
    


