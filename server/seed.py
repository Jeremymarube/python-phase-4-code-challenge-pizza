#!/usr/bin/env python3
from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

with app.app_context():
    print("Deleting data...")
    RestaurantPizza.query.delete()
    Pizza.query.delete()
    Restaurant.query.delete()

    print("Creating restaurants...")
    shack = Restaurant(name="Karen's Pizza Shack", address="123 Main Street")
    bistro = Restaurant(name="Sanjay's Pizza", address="456 Market Road")
    palace = Restaurant(name="Kiki's Pizza", address="789 Sunset Blvd")

    print("Creating pizzas...")
    cheese = Pizza(name="Cheese", ingredients="Dough, Tomato Sauce, Cheese")
    pepperoni = Pizza(
        name="Pepperoni", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni"
    )
    california = Pizza(
        name="California", ingredients="Dough, Sauce, Ricotta, Red Peppers, Mustard"
    )

    print("Creating restaurant_pizzas...")
    pr1 = RestaurantPizza(restaurant=shack, pizza=cheese, price=10)
    pr2 = RestaurantPizza(restaurant=bistro, pizza=pepperoni, price=15)
    pr3 = RestaurantPizza(restaurant=palace, pizza=california, price=20)

    db.session.add_all([shack, bistro, palace, cheese, pepperoni, california, pr1, pr2, pr3])
    db.session.commit()

    print("✅ Seeding done!")
