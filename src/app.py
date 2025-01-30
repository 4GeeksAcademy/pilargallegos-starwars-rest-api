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
from models import db, User, Species, Planets, People
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

@app.route('/user', methods = ['GET'])
def get_all_users():
    user_list = User.query.all()
    response_body = {
        "content": user_list
    }
    return jsonify(response_body), 200

@app.route('/user/<int:user_id>', methods = ['GET'])
def handle_get_user(user_id):
    user = User.query.get(user_id)
    response_body = {
        "content": user
    }
    return jsonify(response_body), 200

@app.route('/species', methods = ['GET'])
def get_all_species():
    species_list = Species.query.all()
    response_body = {
        "content": species_list
    }
    return jsonify(response_body), 200

@app.route('/species/<int:specie_uid>', methods = ['GET'])
def handle_get_specie(specie_id):
    specie = Species.query.get(specie_id)
    response_body = {
        "content": specie
    }
    return jsonify(response_body), 200

@app.route('/planets', methods = ['GET'])
def get_all_planets():
    planets_list = Planets.query.all()
    response_body = {
        "content": planets_list
    }
    return jsonify(response_body), 200

@app.route('/planets/<int:planet_uid>', methods = ['GET'])
def handle_get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    response_body = {
        "content": planet
    }
    return jsonify(response_body), 200

@app.route('/people', methods = ['GET'])
def get_all_people():
    people_list = People.query.all()
    response_body = {
        "content": people_list
    }
    return jsonify(response_body), 200

@app.route('/people/<int:person_uid>', methods = ['GET'])
def handle_get_person(person_uid):
    person = People.query.get(person_uid)
    response_body = {
        "content": person
    }
    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
