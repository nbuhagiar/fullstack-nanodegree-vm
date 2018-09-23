#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify, flash
from database_setup import Base, Restaurant, MenuItem
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///restaurantmenu.db"
db = SQLAlchemy(app)

@app.route("/")
@app.route("/restaurants/")
def showRestaurants():
  restaurants = db.session.query(Restaurant).all()
  return render_template("restaurants.html", restaurants=restaurants)

@app.route("/restaurants/JSON")
def showRestaurantsJSON():
  restaurants = db.session.query(Restaurant).all()
  return jsonify([restaurant.serialize for restaurant in restaurants])

@app.route("/restaurant/new/", methods=["GET", "POST"])
def newRestaurant():
  if request.method == "POST":
    restaurant = Restaurant(name=request.form["name"])
    db.session.add(restaurant)
    db.session.commit()
    flash("New Restaurant Created")
    return redirect(url_for("showRestaurants"))
  else:
    return render_template("newrestaurant.html")

@app.route("/restaurant/<int:restaurant_id>/")
@app.route("/restaurant/<int:restaurant_id>/menu/")
def showMenu(restaurant_id):
  restaurant = (db.session.query(Restaurant)
                          .filter_by(restaurant_id=restaurant_id)
                          .one())
  items = (db.session.query(MenuItem)
                     .filter_by(restaurant_id=restaurant.restaurant_id))
  return render_template("menu.html", restaurant=restaurant, items=items)

@app.route("/restaurant/<int:restaurant_id>/JSON")
@app.route("/restaurant/<int:restaurant_id>/menu/JSON")
def showMenuJSON(restaurant_id):
  restaurant = (db.session.query(Restaurant)
                          .filter_by(restaurant_id=restaurant_id)
                          .one())
  items = (db.session.query(MenuItem)
                     .filter_by(restaurant_id=restaurant.restaurant_id))
  return jsonify([item.serialize for item in items])

@app.route("/restaurant/<int:restaurant_id>/<int:menu_id>/JSON")
@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON")
def showMenuItemJSON(restaurant_id, menu_id):
  restaurant = (db.session.query(Restaurant)
                          .filter_by(restaurant_id=restaurant_id)
                          .one())
  item = (db.session.query(MenuItem)
                    .filter_by(restaurant_id=restaurant.restaurant_id, 
                               menu_id=menu_id)).one()
  return jsonify(item.serialize)

@app.route("/restaurant/<int:restaurant_id>/edit/", methods=["GET", "POST"])
def editRestaurant(restaurant_id):
  restaurant = (db.session.query(Restaurant)
                          .filter_by(restaurant_id=restaurant_id)
                          .one())
  if request.method == "POST":
    if request.form["name"]:
      restaurant.name = request.form["name"]
    db.session.add(restaurant)
    db.session.commit()
    flash("Restaurant Successfully Edited")
    return redirect(url_for("showMenu", restaurant_id=restaurant_id))
  else:
    return render_template("editrestaurant.html", restaurant=restaurant)

@app.route("/restaurant/<int:restaurant_id>/delete/", methods=["GET", "POST"])
def deleteRestaurant(restaurant_id):
  restaurant = (db.session.query(Restaurant)
                          .filter_by(restaurant_id=restaurant_id)
                          .one())
  if request.method == "POST":
    db.session.delete(restaurant)
    db.session.commit()
    flash("Restaurant Successfully Deleted")
    return redirect(url_for("showRestaurants"))
  else:
    return render_template("deleterestaurant.html", restaurant=restaurant)

@app.route("/restaurant/<int:restaurant_id>/menu/new/", methods=["GET", "POST"])
def newMenuItem(restaurant_id):  
  if request.method == "POST":
    item = MenuItem(name=request.form["name"], 
                    description=request.form["description"], 
                    price=request.form["price"], 
                    course=request.form["course"], 
                    restaurant_id=restaurant_id)
    db.session.add(item)
    db.session.commit()
    flash("Menu Item Created")
    return redirect(url_for("showMenu", restaurant_id=restaurant_id))
  else:
    return render_template("newmenuitem.html", restaurant_id=restaurant_id)

@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/", 
           methods=["GET", "POST"])
def editMenuItem(restaurant_id, menu_id):
  restaurant = (db.session.query(Restaurant)
                          .filter_by(restaurant_id=restaurant_id)
                          .one())
  item = (db.session.query(MenuItem)
                    .filter_by(restaurant_id=restaurant.restaurant_id, 
                               menu_id=menu_id)).one()
  if request.method == "POST":    
    if request.form["name"]:
      item.name = request.form["name"]
    db.session.add(item)
    db.session.commit()
    flash("Menu Item Successfully Edited")
    return redirect(url_for("showMenu", restaurant_id=restaurant_id))
  else:
    return render_template("editmenuitem.html", restaurant=restaurant, item=item)

@app.route("/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/", 
           methods=["GET", "POST"])
def deleteMenuItem(restaurant_id, menu_id):
  restaurant = (db.session.query(Restaurant)
                          .filter_by(restaurant_id=restaurant_id)
                          .one())
  item = (db.session.query(MenuItem)
                    .filter_by(restaurant_id=restaurant.restaurant_id, 
                               menu_id=menu_id)).one()
  if request.method == "POST":    
    db.session.delete(item)
    db.session.commit()
    flash("Menu Item Successfully Deleted")
    return redirect(url_for("showMenu", restaurant_id=restaurant_id))
  else:
    return render_template("deletemenuitem.html", restaurant=restaurant, item=item)

if __name__ == "__main__":
  app.secret_key = "super_secret_key"
  app.debug = True
  app.run(host="0.0.0.0", port=5000)