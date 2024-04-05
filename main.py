from flask import Flask, render_template, request, url_for, redirect, session

import pymongo
import os
import bcrypt

app = Flask("IVetCom")
mongo = pymongo.MongoClient(os.getenv("MONGO_KEY"))
app.secret_key = os.getenv("COOKIES_KEY")


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

@app.route('/register', methods=['POST', 'GET'])
def register():
    # Si on essaye de soumettre un formulaire
    if request.method == 'POST':
      # On verifie qu'un utilisateur du meme nom n'existe pas
      db_utils = mongo.db.utilisateurs
      # Si l'utilisateur existe déja on demande de re-remplir le formulaire
      if (db_utils.find_one({'pseudo': request.form['pseudo']})):
        return render_template('register.html',
                               erreur="Ce pseudo existe deja")
      # Sinon on créé l'utilisateur
      else:
        if (request.form['mot_de_passe'] == request.form['verif_mot_de_passe']):
          # On crypte le mot de passe
          mdp_encrypte = bcrypt.hashpw(
            request.form['mot_de_passe'].encode('utf-8'), bcrypt.gensalt())
          # On ajoute l'utilisateur
          db_utils.insert_one({
            'nom': request.form['nom'],
            'prenom': request.form['prenom'],
            'pseudo': request.form['pseudo'],
            'mdp': mdp_encrypte,
            'email': request.form['email'],
            'numero_de_tel': request.form['numero_de_tel'],
            'role': "abonné"
          })
          # On le connecte
          session['util'] = request.form['pseudo']
          # On retourne à la page d'accueil
          return redirect(url_for('index'))
        # Sinon on renvoie le template vide et met un message d'erreur
        else:
          return render_template(
            'register.html', erreur="Les mots de passe doivent être identiques")
    else:
      return render_template('register.html')



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