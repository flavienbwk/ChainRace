from flask import Flask, request, session, jsonify
from db import Database, UserDB, VehiculeDB, ContestDB
from bson import json_util
import requests, json

app = Flask(__name__)
app.secret_key = 'yolo'

if __name__ == '__main__':
    app.run(debug=True)

def getDB():
    return Database.connectDB()

@app.route('/')
def index():
    return jsonify({'message': 'root'})

@app.route('/register', methods=['POST']) #CERTIFIED
def register():
    if request.method == 'POST':
        formulaire = request.json
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

@app.route('/login', methods=['POST']) #CERTIFIED
def login():
    if request.method == 'POST':
        try:
            form = request.json
            if UserDB.checkUser(form['username'], form['password']):
                session['user'] = form['username']
                return jsonify({'message': 'logged in'})
            else:
                return jsonify({'message': 'Wrong Informations'})
        except Exception as e:
            return jsonify({'message': str(e)})
    else:
        return jsonify({'message': 'Bad Request Method'})


# user
@app.route('/user/<user_username>/assign/<vehicule_name>', methods=['GET']) #CERTIFIED
def assign_vehicule_to_user(user_username, vehicule_name):
    if request.method == 'GET':
        try:
            assignement = UserDB.assign_vehicule_to_user(user_username, vehicule_name)
            if assignement == 'checked':
                return jsonify({'message': 'vehicule assigned successfully'})
            else:
                return jsonify({'error' : assignement})
        except Exception as e:
            return jsonify({'message': str(e)})
    else:
        return jsonify({'message': 'Bad Request Method'})

@app.route('/user/<user_username>/reward/<nb_tokens>', methods=['POST']) # pinged par l'API d'Eliot #ALMOST CERTIFIED
def reward_user_with_tokens(user_username, nb_tokens):
    if request.method == 'POST':
        newform = request.json
        description = newform.get('desc')
        try:
            tokens_given = UserDB.reward_with_token(user_username, nb_tokens, description)
            return jsonify({'message': tokens_given})
        except Exception as e:
            return jsonify({'message': str(e)})
    else:
        return jsonify({'message': 'bad request method'})

@app.route('/user/<user_username>/get/all/models', methods=['GET'])
def get_all_models(user_username):
    if request.method == 'GET':
        try:
            models = UserDB.get_all_models(user_username)
            return jsonify({'message': models})
        except Exception as e:
            return jsonify({'message': str(e)})
    else:
        return jsonify({'message': 'wrong method'})


@app.route('/user/get/won/money', methods=['GET']) #ALMOST CERTIFIED
def get_won_money():

    if request.method == 'GET':
        try:
            users = json.loads(json.dumps(list(UserDB.get_won_money()), default=json_util.default))
            n = 0
            for user in users:
                total = 0
                if "tokens" in user:
                    for i in user['tokens']:
                        total += int(i[0])
                users[n]['total'] = total
                del users[n]['password']
                n += 1
            return json.dumps({'message': users})
        except Exception as e:
            return jsonify({'message': str(e)})
    else:
        return jsonify({'message': 'wrong method'})


@app.route('/user/<user_username>/get/all/money', methods=['POST'])
def request_eliot_for_tokens(user_username):

    if request.method == 'POST':
        try:
            user = UserDB.getOneUser(user_username)
            url = 'http:eliotctl.fr/interact_blockchain/ask/money'
            payload = jsonify({'username': user_username, 'public_key': user['public_key'], 'token': 'ULTIMATE_TOKEN'})
            response = requests.request("POST", url, data=payload).text
            return jsonify({'message': response})
        except Exception as e:
            return jsonify({'message': str(e)})
    else:
        return jsonify({'message': 'wrong method'})


# vehicule
# @app.route('/vehicule/create', methods=['POST'])
# def add_car():
#     if request.method == 'POST':
#         formulaire = request.form
#         try:
#             vehicule = {'username': formulaire['username']}
#             vehiculeID = VehiculeDB.saveNewVehicule(vehicule)
#             if vehiculeID is not None:
#                 return jsonify({'message': vehiculeID})
#             else:
#                 return jsonify({'message': 'ID already in use or no user found'})
#         except Exception as e:
#             return jsonify({'message': str(e)})
#     else:
#         return jsonify({'message': 'Bad Request Method'})


# contest
@app.route('/contest/create/by/<user_username>', methods=['POST'])# CERTIFIED
def create_contest(user_username):
    if request.method == 'POST':
        try:
            newform = request.json
            infos = {'name': newform['name'], 'ends_days': newform['ends_days'], 'ends_hours': newform['ends_hours']}
            contestCreation = UserDB.create_contest(user_username, infos)
            return jsonify({'message': contestCreation})
        except Exception as e:
            return jsonify({'message': str(e)})
    else:
        return jsonify({'message': 'Bad Request Method'})

@app.route('/contest/get/all', methods=['GET']) #CERTIFIED
def get_all_contest():
    if request.method == 'GET':
        try:
            contests = ContestDB.get_all_contests()
            return contests
        except Exception as e:
            return jsonify({'message': str(e)})
    else:
        return jsonify({'message': 'Bad Request Method'})

@app.route('/model/new/from/vehicule', methods=['POST']) #ALMOST CERTIFIED
def get_model_fron_vehicule():
    if request.method == 'POST':
        try:
            newform = request.json
            model = newform['model']
            user_username = newform['username']
            if UserDB.add_model_from_vehicule(model, user_username):
                user = UserDB.getOneUser(user_username)
                url = 'http:eliotctl.fr/api/add/model'
                payload = jsonify({'username': user_username, 'public_key': user['public_key'], 'model': model, 'token': 'ULTIMATE_TOKEN'})
                response = requests.request("POST", url, data=payload).text
                return jsonify({'message': response})
            else:
                return jsonify({'message': 'couldnt add the model'})
        except Exception as e:
            return jsonify({'message': str(e)})
    else:
        return jsonify({'message': 'Bad Request Method'})

@app.route('/model/new/by/<user_username>', methods=['POST']) #ALMOST CERTIFIED
def get_new_model(user_username):
    if request.method == 'POST':
        try:
            newform = request.json
            model = newform['model']
            UserDB.add_model(user_username, model)
            return jsonify({'message': 'model created'})
        except Exception as e:
            return jsonify({'message': str(e)})
    else:
        return jsonify({'message': 'bad request method'})