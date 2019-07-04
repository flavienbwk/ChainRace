from flask import Flask, request, session, jsonify
from db import Database, UserDB, VehiculeDB, ContestDB

app = Flask(__name__)
app.secret_key = 'yolo'

if __name__ == '__main__':
    app.run(debug=True)

def getDB():
    return Database.connectDB()

@app.route('/')
def index():
    return jsonify({'message': 'root'})

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        formulaire = request.form
        try:
            user = dict({'username': formulaire['username'], 'password': formulaire['password'], 'email': formulaire['email']})
            if UserDB.saveNewUser(user) == True:
                return jsonify({'message': 'User Registered'})
            else:
                return jsonify({'message': 'User already exists'})
        except Exception as e:
            return jsonify({'message': str(e)})
    else:
        return jsonify({'message': 'Bad Request Method'})

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            if UserDB.checkUser(username, password):
                session['user'] = username
                return jsonify({'message': 'logged in'})
            else:
                return jsonify({'message': 'Wrong Informations'})
        except Exception as e:
            return jsonify({'message': str(e)})
    else:
        return jsonify({'message': 'Bad Request Method'})


# user
@app.route('/user/<user_username>/assign/<vehicule_public_id>', methods=['GET'])
def assign_vehicule_to_user(user_username, vehicule_public_id):
    try:
        assignement = UserDB.assign_vehicule_to_user(user_username, vehicule_public_id)
        if assignement == 'checked':
            return jsonify({'message': 'vehicule assigned successfully'})
        else:
            return jsonify({'error' : assignement})
    except Exception as e:
        return jsonify({'message': str(e)})
    return jsonify({'message': 'Bad Request Method'})


@app.route('/user/<user_public_id>/reward/<nb_tokens>', methods=['POST']) # Add tokens to user POST <user>,<nb token> // ping API d'Eliot
def reward_user_with_tokens(user_public_id, nb_tokens):
    # if request.method == 'POST':
    return ''

@app.route('/user/<user_username>/get/all/models', methods=['GET']) # Liste de tous les models from un user GET <user ID>
def get_all_models(user_username):
    if request.method == 'GET':
        try:
            models = UserDB.get_all_models(user_username)
            return jsonify({'message': models})
        except Exception as e:
            return jsonify({'message': str(e)})
    return jsonify({'message': 'wrong method'})

# vehicule
@app.route('/vehicule/create', methods=['POST'])
def add_car():
    if request.method == 'POST':
        formulaire = request.form
        try:
            vehicule = dict({'username': formulaire['username'], 'id': formulaire['id']})
            if VehiculeDB.saveNewVehicule(vehicule) == True:
                return jsonify({'message': 'Vehicule Created'})
            else:
                return jsonify({'message': 'ID already in use or no user found'})
        except Exception as e:
            return jsonify({'message': str(e)})
    else:
        return jsonify({'message': 'Bad Request Method'})

# contest
@app.route('/contest/create/by/<user_username>', methods=['POST']) # Creation de competition POST <compet’ ID>, <user ID>
def create_contest(user_username):
    if request.method == 'POST':
        try:
            infos = {'name': request.form.get('name'), 'starts_at': request.form.get('starts_at')}
            contestCreation = UserDB.create_contest(user_username, infos)
            return jsonify({'message': contestCreation})
        except Exception as e:
            return jsonify({'message': str(e)})
    else:
        return jsonify({'message': 'Bad Request Method'})

@app.route('/contest/get/all', methods=['GET'])
def get_all_contest():
    if request.method == 'GET':
        try:
            contests = ContestDB.get_all_contests()
            return jsonify({'message': contests})
        except Exception as e:
            return jsonify({'message': str(e)})
    else:
        return jsonify({'message': 'Bad Request Method'})