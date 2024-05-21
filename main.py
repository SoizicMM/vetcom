from flask import Flask, render_template, request, url_for, redirect, session

import pymongo
import os
import bcrypt

app = Flask("IVetCom")
mongo = pymongo.MongoClient(os.getenv("MONGO_KEY"))
app.secret_key = os.getenv("COOKIES_KEY")

# ACCUEIL
@app.route("/")
def index():
  return render_template("index.html")


# UTILISATEURS
@app.route('/login', methods=['POST', 'GET'])
def login():
    # si on essaye de se connecter ca veut dire qu'on viens dans la methode POST
    if request.method == 'POST':
      db_utils = mongo.db.utilisateurs
      util = db_utils.find_one({'email': request.form['email']})
      #si l'utilisateur existe 
      if util:
        #verification du mdp
        if bcrypt.checkpw(request.form['mot_de_passe'].encode('utf-8'),util['mdp']): 
          session['util'] = request.form['email']
          return redirect(url_for("index"))
        #sinon le mdp est incorrect
        else: 
          return render_template('login.html', erreur= "le mot de passe est incorrect")
      #sinon l'utilisateur n'existe pas 
      else:
        return render_template('login.html', erreur = "l'utilisateur n'existe pas")
    else: 
      return render_template('login.html')

     
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
@app.route("/femme")
def femme():
  db_femme = mongo.db.femme
  femme = db_femme.find({})
  return render_template("femme.html", femme=femme)

@app.route("/homme")
def homme():
  db_homme = mongo.db.homme
  homme = db_homme.find({})
  return render_template("homme.html", homme=homme)

@app.route("/enfant")
def enfant():
  db_enfant = mongo.db.enfant
  enfant = db_enfant.find({})
  return render_template("enfant.html", enfant=enfant)

@app.route("/accessoire")
def accessoire():
  db_accessoire = mongo.db.accessoire
  accessoire = db_accessoire.find({})
  return render_template("accessoire.html", accessoire=accessoire)


#AUTRE
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

@app.route("/settings")
def settings():
  return render_template("settings.html")

@app.route("/cookies")
def cookies():
  return render_template("cookies.html")


app.run(host="0.0.0.0", port=3904) 