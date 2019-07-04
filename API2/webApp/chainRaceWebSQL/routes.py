from flask import request, jsonify
from chainRaceWeb import app
from chainRaceWeb.sql_obj import sql
# from chainRaceWeb.models import User, Vehicule, Model, Wallet, Contest, Race, Stat
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import uuid, jwt, datetime

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'}), 403

        return f(current_user, *args, **kwargs)
    return decorated



@app.route('/')
def hello_world():
    return 'Hello, World!'

# register senseY etre fonctionnel
@app.route('/register', methods=['POST'])
def register():
    public_id = str(uuid.uuid4())
    username = request.form.get('username')
    email = request.form.get('email')
    hashed_password = generate_password_hash(request.form.get('password'), method='sha256')
    if sql.get("SELECT * FROM user where username=%s", (request.form.get('username')))[0] is not None:
        return jsonify({'message' : 'username already used'})
    # cur = mysql.connection.cursor()
    # cur.execute("INSERT INTO user(ids, username, email, password) VALUES (%s, %s, %s, %s)", (public_id, username, email, hashed_password))
    sql.post("INSERT INTO user(ids, username, email, password) VALUES (%s, %s, %s, %s)", (public_id, username, email, hashed_password))
    # mysql.connection.commit()
    # cur.close()
    return sql.get("SELECT * FROM user where username=%s", (request.form.get('username')))

# login senseY etre fonctionnel
@app.route('/login', methods=['POST'])
def login():
    auth = request.form
    # cur = mysql.connection.cursor()
    # user = cur.execute("SELECT * FROM user where username=" + auth.get('username'))
    user = sql.get("SELECT * FROM user where username=%s", (auth.get('username')))[0]
    # mysql.connection.commit()
    # cur.close()
    if user is None:
        return jsonify({'message' : 'invalid username'})
    elif not check_password_hash(user.get('hash_password'), auth.get('password')):
        return jsonify({'message' : 'invalid password'})
    else:
        token = jwt.encode({'public_id' : auth.get('public_id'), 'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})
    return jsonify({'message' : 'didnt go in any loop. gotta investigate that quickly'})

# route senseY etre fonctionnelle
@app.route('/users/get/all')
@token_required
def get_all_users(current_user):
    cur = mysql.connection.cursor()
    resValue = cur.execute("SELECT * FROM users")
    if resValue > 0:
        userDetails = cur.fetchall()
    cur.close()
    return userDetails

# route senseY etre fonctionnelle
@app.route('/users/get/<public_id>')
@token_required
def get_one_user(current_user, public_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users where ids=" + public_id)
    user = cur.fetchone()
    cur.close()
    if not user:
        return jsonify({'message': 'user not found'})
    return jsonify({'user': user})

# route senseY etre fonctionnelle
@app.route('/users/delete/<public_id>', methods=['DELETE'])
@token_required
def delete_one_user(current_user, public_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users where ids=" + public_id)
    user = cur.fetchone()
    if not user:
        return jsonify({'message': 'user not found'})
    cur.execute("DELETE FROM users where ids=" + public_id)
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'user deleted'})


#User

@app.route('/user/<user_public_id>/assign/<vehicule_public_id>', methods=['POST']) # C
def assign_vehicule_to_user(user_public_id, vehicule_public_id):
    return ''

# @app.route('/user/<user_public_id>/resign/<vehicule_public_id>', methods=['POST']) # C
# def resign_vehicule_from_user(user_public_id, vehicule_public_id):
#     return ''

@app.route('/user/<user_public_id>/reward/<nb_tokens>', methods=['POST']) # Add tokens to user POST <user>,<nb token>
def reward_user_with_tokens(user_public_id, nb_tokens):
    return ''

@app.route('/user/get/all/about/tokens', methods=['GET']) # Retourne tous les users selon leur nombre de tokens gagnés décroissant GET
def get_all_users_in_most_token_order():
    return ''

@app.route('/user/<user_public_id>/get/all/tokens', methods=['GET']) #Retourne nb de token gagné + nb de token sur le wallet GET <user ID>
def get_all_tokens_from_user(user_public_id):
    return ''

@app.route('/user/get/all/models', methods=['GET']) # Liste de tous les models from un user GET <user ID>
def get_all_models(current_user_id):
    return ''

@app.route('/user/update/wallet', methods=['POST']) # Modification passphrase, clé publique, adresse POST <user ID>, <passphrase>, <public key>, <address> ?? je dois contacter l'API d'Eliot
def update_user_wallet(current_user_id, passphrase, public_key, address):
    return ''


# Vehicule

@app.route('/vehicule/create')
@token_required
def create_vehicule(current_user):
    return ''

@app.route('/vehicule/claim/<userid>', methods=['POST'])
@token_required
def claim_vehicule(current_user, userid):
    return ''

@app.route('/vehicule/get/from/<user_public_id>', methods=['GET']) # C
def get_vehicules_from(user_public_id):
    return ''

@app.route('/vehicule/<vehicule_public_id>/assign/model/<model_public_id>', methods=['POST']) # Assignation d’un model à un vehicule POST < ,,,,,, >, <vehicule ID>
def assign_model_to_vehicule(vehicule_public_id, model_public_id):
    return ''


#Contest

@app.route('/contest/create', methods=['POST']) # Creation de competition POST <compet’ ID>, <user ID>
def create_contest(current_user_id):
    return ''

@app.route('contest/<contest_public_id>/get/leaderboard', methods=['GET']) # Retourne nom, classement compet’ GET <compet’ ID> en fonction du temps
def get_contest_leaderboard(contest_public_id):
    return ''

@app.route('/contest/<contest_public_id>/add/vehicule/<vehicule_public_id>', methods=['POST']) # Ajout d’un vehicule à une compet’ POST <compet’ ID>, <vehicule ID>
def add_vehicule_to_contest(contest_public_id, vehicule_public_id):
    return ''


#Model

@app.route('/model/new/<path>', methods=['POST']) # Upload de model POST <file>, <user ID>
def upload_model(path, current_user_id):
    return ''


#Race

@app.route('race/set/stats', methods=['POST']) # C
def set_race_stats():
    return ''



@app.route('/') #Retourne les stats d’un vehicule GET <user ID>/<vehicule ID> ??