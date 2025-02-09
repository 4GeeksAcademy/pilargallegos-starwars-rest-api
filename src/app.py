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
from models import db, User, Species, Planets, People, Favorites
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

@app.route('/user/<int:user_id>', methods = ['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"error": "User not found"}),404

@app.route('/user', methods = ['POST'])
def add_user():
    data = request.get_json()
    required_fields={"name", "email", "password"}
    if not all(field in data for field in required_fields):
        return jsonify({"error":"Missing required fields"}), 400
    new_user = User (
        id = data["id"],
        name = data["name"],
        email = data["email"],
        password = data["password"]
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user), 201

@app.route('/species', methods=['POST'])
def new_specie():
    data = request.get_json()
    required_fields = {"uid", "description", "name", "homeworld"}
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    new_specie = Species (
        uid = data["uid"],
        description = data["description"],
        name = data["name"],
        homeworld = data["homeworld"]
    )
    db.session.add(new_specie)
    db.session.commit()

    return jsonify(new_specie), 201

@app.route('/species', methods = ['GET'])
def get_all_species():
    species_list = Species.query.all()
    response_body = {
        "content": species_list
    }
    return jsonify(response_body), 200

@app.route('/species/<int:specie_uid>', methods = ['GET', 'DELETE'])
def handle_specie(specie_uid):
    if request.method == "DELETE":
        specie = Species.query.get(specie_uid)        
        if specie:
            db.session.delete(specie)
            db.session.commit()
            return jsonify({"message": "Specie deleted"}), 200
        else:
            return jsonify({"error":"Specie not found"}),404
    else:
        specie = Species.query.get(specie_uid)
        if specie:
            return jsonify({"content": specie}), 200
        else:    
            return jsonify({"error": "Specie not found"}), 404

@app.route('/planets', methods = ['GET'])
def get_all_planets():
    planets_list = Planets.query.all()
    response_body = {
        "content": planets_list
    }
    return jsonify(response_body), 200

@app.route('/planets/<int:planet_uid>', methods = ['GET'])
def handle_get_planet(planet_uid):
    planet = Planets.query.get(planet_uid)
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

@app.route('/people/<int:person_uid>', methods = ['GET', 'DELETE'])
def handle_person(person_uid):
    if request.method == "DELETE":
        person = People.query.get(person_uid)        
        if person:
            db.session.delete(person)
            db.session.commit()
            return jsonify({"message": "Person deleted"}), 200
        else:
            return jsonify({"error":"Person not found"}),404
    else:
        person = People.query.get(person_uid)
        if person:
            return jsonify({"content": person}), 200
        else:    
            return jsonify({"error": "Person not found"}), 404

@app.route('/people', methods=['POST'])
def new_person():
    data = request.get_json()
    required_fields = {"uid", "name", "description", "homeworld"}
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    new_person = People (
        uid = data["uid"],
        name = data["name"],
        description = data["description"],
        homeworld = data["homeworld"]
    )
    db.session.add(new_person)
    db.session.commit()

    return jsonify(new_person), 201

@app.route('/favorites', methods =['GET'])
def get_favorites():
    favorite_list = Favorites.query. all()
    response_body = {
        "content": favorite_list
    }
    return jsonify(response_body), 200

@app.route('/favorites', methods =['POST'])
def add_favorite():
    data = request.get_json()
    print("Received data:", data)
    required_fields = {"external_id", "type", "name"}
    if not all(field in data for field in required_fields):
        return jsonify ({"error": "Missing required fields"}), 400
    
    user_id=1
    new_favorite = Favorites (
        external_id =  data["external_id"],
        type = data["type"],
        name = data["name"],
        user_id = user_id
    )
    db.session.add(new_favorite)
    db.session.commit()
    
    return jsonify(new_favorite), 201

@app.route('/favorites/<int:id>', methods = ['DELETE'])
def delete_favorite(id):
  favorite = Favorites.query.get(id)
  if not favorite:
      return jsonify({"error": "Favorite not found"}), 404
  db.session.delete(favorite)
  db.session.commit()

  return jsonify({"message": "Favorite deleted"}), 200


    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
