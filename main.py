from flask import Flask, render_template, request, url_for, redirect, session
import pymongo
import os
import bcrypt

app = Flask("Vetcom")
mongo = pymongo.MongoClient(os.getenv("MONGO_KEY"))
app.secret_key = os.getenv("COOKIES_KEY")
confidentiality_code = os.environ['titi']

# ACCUEIL
@app.route("/")
def index():
    return render_template("index.html")

#ERRUER 404
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404
    
# UTILISATEURS
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        db_utils = mongo.db.utilisateurs
        util = db_utils.find_one({'email': request.form['email']})
        if util and bcrypt.checkpw(request.form['mot_de_passe'].encode('utf-8'), util['mdp']):
            session['util'] = request.form['email']
            return redirect(url_for("index"))
        else:
            erreur = "Le mot de passe est incorrect" if util else "L'utilisateur n'existe pas"
            return render_template('login.html', erreur=erreur)
    else:
        return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        db_utils = mongo.db.utilisateurs
        if db_utils.find_one({'pseudo': request.form['pseudo']}):
            return render_template('register.html', erreur="Ce pseudo existe déjà")
        if request.form['mot_de_passe'] == request.form['verif_mot_de_passe']:
            mdp_encrypte = bcrypt.hashpw(request.form['mot_de_passe'].encode('utf-8'), bcrypt.gensalt())
            db_utils.insert_one({
                'nom': request.form['nom'],
                'prenom': request.form['prenom'],
                'pseudo': request.form['pseudo'],
                'mdp': mdp_encrypte,
                'email': request.form['email'],
                'numero_de_tel': request.form['numero_de_tel'],
                'role': "abonné"
            })
            session['util'] = request.form['pseudo']
            return redirect(url_for('index'))
        else:
            return render_template('register.html', erreur="Les mots de passe doivent être identiques")
    else:
        return render_template('register.html')

@app.route("/logout")
def logout():
    session.pop('util', None)
    return redirect(url_for("index"))

# FRONT
@app.route("/categories")
def categories():
    return render_template("categories.html")

@app.route("/panier")
def panier():
    db_enfant = mongo.db.enfant
    enfant = db_enfant.find({})
    return render_template("panier.html", enfant=enfant)

# CATEGORIES
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

# ASSISTANCE
@app.route("/assistance")
def assistance():
    return render_template("assistance.html")

# AUTRE
@app.route("/validation")
def validation():
    return render_template("validation.html")

@app.route("/payment", methods=["GET", "POST"])
def payment():
    if request.method == "POST":
        total_amount = request.form.get('totalAmount', default="0")
        return render_template("payment.html", total_amount=total_amount)
    return render_template("cart.html")

@app.route('/adm')
def adm_page():
    return render_template('adm.html')

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/cookies")
def cookies():
    return render_template("cookies.html")







# ADMINISTRATION
@app.route("/envoyer_message", methods=["POST"])
def envoyer_message():
    try:
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        email = request.form["email"]
        objet = request.form["objet"]
        date_envoi = request.form["date_envoi"]
        texte = request.form["texte"]

        db_message = mongo.db.message
        db_message.insert_one({
            "nom": nom,
            "prenom": prenom,
            "email": email,
            "objet": objet,
            "date_envoi": date_envoi,
            "texte": texte
        })

        return redirect(url_for("index"))
    except Exception as e:
        return str(e)


@app.route('/administration')
def administration():
    return render_template('administration.html')

@app.route('/loginn', methods=['POST'])
def loginn():
    code = request.form.get('code')
    if code == confidentiality_code:
        # Authentification réussie, rediriger vers la page d'administration sécurisée
        return  redirect(url_for('secure_administration'))
    else:
    # Mauvais code, rediriger vers la page d'administration avec un message d'erreur
        return redirect(url_for('administration_error'))

@app.route('/administration_error')
def administration_error():
    return render_template('error.html')

@app.route('/secure_administration')
def secure_administration():
    # Code pour la page d'administration sécurisée
    db_message = mongo.db.message
    message = db_message.find({})
    db_commande = mongo.db.commande
    commande = db_commande.find({})
    return render_template('/administrationadmin.html', message=message, commande=commande)










if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3904)
