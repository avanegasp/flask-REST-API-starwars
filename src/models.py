from flask_sqlalchemy import SQLAlchemy
from enum import Enum as SQLEnum


db = SQLAlchemy()

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
    suscription_date = db.Column(db.DateTime, nullable=False)

    signIns = db.relationship("SignIn", backref="user")
    planetsFavorites = db.relationship("PlanetFavorite", backref="user")
    charactersFavorites = db.relationship("CharacterFavorite", backref="user")
    starshipsFavorite = db.relationship("StarshipFavorite", backref="user")

    def __repr__(self):
        return "<User %r>" % self.id
    
    def serialize(self):
        return{
            "id":self.id,
            "name":self.name,
            "last_name":self.last_name,
            "gender":self.gender.value,
            "email":self.email,
            "suscription_date":self.suscription_date
        }

class SignIn(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Date, nullable=False) 

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return "<SignIn %r>" % self.id
    
    def serialize(self):
        return{
            "id": self.id,
            "timestamp": self.timestamp
        }

class Character(db.Model):   

    id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String(100), nullable=False)
    character_gender = db.Column(db.String(50), nullable=False)
    hair_color = db.Column(db.String(50), nullable=False)
    eyes_color = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return "<Character %r>" % self.id
    
    def serialize(self):
        return{
            "id": self.id,
            "character_name": self.character_name,
            "character_gender": self.character_gender,
            "hair_color": self.hair_color,
            "eyes_color": self.eyes_color
        }

class Planet(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String(100), nullable=False)
    population = db.Column(db.String(100), nullable=False)
    terrain = db.Column(db.String(100), nullable=False)
    surface_water = db.Column(db.String(100), nullable=False)
    gravity = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<Planet %r>" % self.id
    
    def serialize(self):
        return{
            "id": self.id,
            "planet_name": self.planet_name,
            "population": self.population,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "gravity": self.gravity
        }
class Starship(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    starship_name = db.Column(db.String, nullable="False")
    model = db.Column(db.String, nullable="False")
    manufacturer = db.Column(db.String, nullable="False")

    def __repr__(self):
        return "<Starship %r>" % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "starship_name": self.starship_name,
            "model": self.model,
            "manufacturer": self.manufacturer
        }

class CharacterFavorite(db.Model):

    id = db.Column(db.Integer, primary_key=True)
  
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"))

    def __repr__(self):
        return "<CharacterFavorite %r>" % self.id
    
    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id
        }

class PlanetFavorite(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))

    def __repr__(self):
        return "<PlanetFavorite %r>" % self.id
    
    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.id,
            "planet_id": self.id
        }

class StarshipFavorite(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))   
    starship_id = db.Column(db.Integer, db.ForeignKey("starship.id"))
    
    def __repr__(self):
        return "<StarshipFavorite %r>" % self.id
    
    def serialize(self):
        return{
            "id": self.id,
            "user_id": self.user_id,
            "starship_id": self.starship_id
        }

