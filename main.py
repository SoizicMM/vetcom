from flask import Flask, render_template, request, url_for, redirect, session 



app = Flask("IVetCom")

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
  return render_template("homme.html")
@app.route("/femme")
def femme():
  return render_template("femme.html")
@app.route("/enfant")
def enfant():
  return render_template("enfant.html")
@app.route("/accessoire")
def accessoire():
  return render_template("accessoire.html")



@app.route("/settings")
def settings():
  return render_template("settings.html")

@app.route("/cookies")
def cookies():
  return render_template("cookies.html")


app.run(host="0.0.0.0", port=3904) 