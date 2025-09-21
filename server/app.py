#!/usr/bin/env python3
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api
from models import db, Restaurant, RestaurantPizza, Pizza
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

@app.route("/")
def index():
    return "<h1>Code challenge</h1>"

# ------------- RESTAURANTS -------------
@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    response = [r.to_dict(rules=("-restaurant_pizzas",)) for r in restaurants]
    return jsonify(response), 200

@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant(id):
    restaurant = db.session.get(Restaurant, id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    response = {
        "id": restaurant.id,
        "name": restaurant.name,
        "address": restaurant.address,
        "restaurant_pizzas": [
            {
                "id": rp.id,
                "price": rp.price,
                "pizza_id": rp.pizza_id,
                "restaurant_id": rp.restaurant_id,
                "pizza": {
                    "id": rp.pizza.id,
                    "name": rp.pizza.name,
                    "ingredients": rp.pizza.ingredients,
                },
            }
            for rp in restaurant.restaurant_pizzas
        ],
    }
    return jsonify(response), 200

@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = db.session.get(Restaurant, id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    db.session.delete(restaurant)
    db.session.commit()
    return "", 204

# ------------- PIZZAS -------------
@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = Pizza.query.all()
    response = [p.to_dict(rules=("-restaurant_pizzas",)) for p in pizzas]
    return jsonify(response), 200

# ------------- RESTAURANT PIZZAS -------------
@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.get_json()
    try:
        new_rp = RestaurantPizza(
            price=data.get("price"),
            pizza_id=data.get("pizza_id"),
            restaurant_id=data.get("restaurant_id"),
        )
        db.session.add(new_rp)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400

    response = {
        "id": new_rp.id,
        "price": new_rp.price,
        "pizza_id": new_rp.pizza_id,
        "restaurant_id": new_rp.restaurant_id,
        "pizza": {
            "id": new_rp.pizza.id,
            "name": new_rp.pizza.name,
            "ingredients": new_rp.pizza.ingredients,
        },
        "restaurant": {
            "id": new_rp.restaurant.id,
            "name": new_rp.restaurant.name,
            "address": new_rp.restaurant.address,
        },
    }
    return jsonify(response), 201

if __name__ == "__main__":
    app.run(port=5555, debug=True)
