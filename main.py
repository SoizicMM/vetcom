from flask import Flask, render_template, request, url_for, redirect, session 

import pymongo
import os


app = Flask("IVetCom")
mongo = pymongo.MongoClient(os.getenv("MONGO_KEY"))

@app.route("/test")
def test():
  db_test = mongo.db.test
  test = db_test.find({})
  return render_template("test.html", test=test)

# ACCUEIL
@app.route("/")
def index():
  return render_template("index.html")


# UTILISATEURS
@app.route("/login")
def login():
  return render_template("login.html")

@app.route("/register")
def register():
  return render_template("register.html")

@app.route("/logout")
def logout():
  return render_template("index.html")


# FRONT
@app.route("/categories")
def categories():
  return render_template("categories.html")

@app.route("/panier")
def panier():
  return render_template("panier.html")


#CATEGORIES
@app.route("/homme")
def homme():
  return render_template("articles.html")
@app.route("/femme")
def femme():
  return render_template("femme.html")
@app.route("/enfant")
def enfant():
  return render_template("enfant.html")
@app.route("/accessoire")
def accessoire():
  return render_template("accessoire.html")

@app.route("/assistance")
def assistance():
  return render_template("assistance.html")
  
@app.route("/validation")
def validation():
  return render_template("validation.html")

@app.route("/payment")
def payment():
  return render_template("payment.html")

@app.route('/adm')
def adm_page():
    return render_template('adm.html')

@app.route('/teset')
def teset():
    return render_template('testperso.html')

@app.route("/settings")
def settings():
  return render_template("settings.html")

@app.route("/cookies")
def cookies():
  return render_template("cookies.html")


app.run(host="0.0.0.0", port=3904) 