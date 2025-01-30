from dataclasses import dataclass
from sqlalchemy import ForeignKey
from flask_sqlalchemy import SQLAlchemy
import enum
db = SQLAlchemy()
@dataclass
class User(db.Model):
    __tablename__ = 'user'
    id:int = db.Column(db.Integer, primary_key=True, index=True, nullable=False)
    name:str = db.Column(db.String(30), nullable=False)
    password:str = db.Column(db.String(30), nullable=False, unique=True)
class FavoritesType(enum.Enum):
    SPECIES = "SPECIES"
    PLANETS = "PLANETS"
    PEOPLE = "PEOPLE"

@dataclass
class Favorites(db.Model):
    __tablename__ = 'favorites'
    id:int = db.Column(db.Integer, primary_key=True, index=True, nullable=False)
    user_id:int = db.Column(db.Integer, ForeignKey('user.id'),index=True, nullable=False)
    external_id:int = db.Column(db.Integer, nullable=False)
    type:str = db.Column(db.Enum(FavoritesType), nullable=False)
    name:str = db.Column(db.String(30), nullable=False)

@dataclass
class Species(db.Model):
    __tablename__ = 'species'
    uid:int = db.Column(db.Integer, primary_key=True, unique=True, index=True, nullable=False)
    description:str = db.Column(db.String(50), nullable=False)
    name:str = db.Column(db.String(30), nullable=False)
    homeworld:int = db.Column(db.Integer, ForeignKey('planets.uid'), nullable=False)

@dataclass
class Planets(db.Model):
    __tablename__ = 'planets'
    uid:int = db.Column(db.Integer, primary_key=True, unique=True, index=True, nullable=False)
    name:str = db.Column(db.String(30), nullable=False)
    gravity:str = db.Column(db.String(100), nullable=False)

@dataclass
class People(db.Model):
    __tablename__ = 'people'
    uid:int = db.Column(db.Integer, primary_key=True, unique=True, index=True, nullable=False)
    description:str = db.Column(db.String(50), nullable=False)
    name:str = db.Column(db.String(30), nullable=False)
    homeworld:int = db.Column(db.Integer, ForeignKey('planets.uid'), nullable=False)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(80), unique=False, nullable=False)
#     is_active = db.Column(db.Boolean(), unique=False, nullable=False)
#     def __repr__(self):
#         return '<User %r>' % self.username
#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }









