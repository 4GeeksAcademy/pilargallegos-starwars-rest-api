from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from flask import Flask
from sqlalchemy import ForeignKey

db = SQLAlchemy()

@dataclass
class User(db.Model):
    __tablename__ = 'user'
    id:int = db.Column(primary_key=True, nullable=False)

@dataclass
class Favorites(db.Model):
    __tablename__ = 'favorites'
    id:int = db.Column( primary_key=True)
    external_id:str = db.Column(db.String(50))
    name:str = db.Column(db.String(50))
    user_id:int = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    type = db.Column(db.Enum('Species', 'Planets', 'People'))

@dataclass
class Species(db.Model):
    __tablename__ = 'species'
    uid:int = db.Column(db.Integer, primary_key=True)
    description:str = db.Column(db.String(250))
    name:str = db.Column(db.String(50))
    homeworld:int = db.Column(db.Integer, ForeignKey('planets.uid'), nullable=False)
    classification:str = db.Column(db.String(50))

@dataclass
class Planets(db.Model):
    __tablename__ = 'planets'
    uid:int = db.Column(db.Integer, primary_key=True)
    name:str = db.Column(db.String(50))
    gravity:str = db.Column(db.String(250))

@dataclass
class People(db.Model):
    __tablename__ = 'people'
    uid:int = db.Column(db.Integer, primary_key=True)
    description:str = db.Column(db.String(250))
    name:str = db.Column(db.String(50))
    homeworld:int = db.Column(db.Integer, ForeignKey('planets.uid'), nullable=False)




    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }