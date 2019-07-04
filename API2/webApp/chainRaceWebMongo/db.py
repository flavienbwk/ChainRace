from pymongo import MongoClient
from bson.json_util import dumps
from flask import jsonify
import uuid, datetime


class Database:

    def connectDB():
        try:
            dbName = 'ChainRace'
            mongoclient = MongoClient('localhost', username='Admin', password='superpassword', authSource=dbName)
            database = mongoclient[dbName]
            print(database)
            return database
        except Exception as e:
            print(e)
            return str(e)


class UserDB:

    def getOneUser(username):
        database = Database.connectDB()
        collection = database['user']
        try:
            user = collection.find({'username': username})
            if len(list(user)) == 1:
                return user
        except Exception as e:
            return str(e)

    def assign_vehicule_to_user(user_username, vehicule_name):
        database = Database.connectDB()
        userCollection = database['user']
        vehiculeCollection = database['vehicule']
        try:
            user = userCollection.find({'username': user_username})
            if len(list(user)) == 1:
                vehicule = vehiculeCollection.insert({'name': vehicule_name})
                userCollection.update({'username' :user_username}, {'$push' : {'vehicule_name': vehicule_name}})
                return 'checked'
            else:
                return 'no user matched'
        except Exception as e:
            return str(e)

    def get_all_models(user_username):
        database = Database.connectDB()
        userCollection = database['user']
        try:
            user = userCollection.find({'username': user_username})
            if len(list(user)) == 1:
                return user['models']
            else:
                return 'user not found'
        except Exception as e:
            return str(e)

    def create_contest(user_username, infos):
        database = Database.connectDB()
        try:
            infos['starts_at'] = str(datetime.datetime.utcnow())
            infos['ends_at'] = str(datetime.datetime.utcnow() + datetime.timedelta(days=int(infos['ends_days']), hours=int(infos['ends_hours'])))
            contest_id = str(uuid.uuid4())
            userCollection = database['user']
            contestCollection = database['contest']
            user = userCollection.find({'username': user_username})
            if infos['name'] is None:
                return 'need a name please'
            elif len(list(contestCollection.find({'name': infos['name']}))) is not 0:
                return 'name already exists'
            if len(list(user)) == 1:
                save = contestCollection.insert({'ids': contest_id, 'name': infos['name'], 'starts_at': infos['starts_at'], 'ends_at': infos['ends_at']})
                userUpd = userCollection.update({'username': user_username}, {'$push' : {'contest_id': contest_id}})
                return 'Contest created'
            else:
                return 'no user found'
        except Exception as e:
            return str(e)

    def reward_with_token(user_username, token_amount, description):
        database = Database.connectDB()
        collection = database['user']
        try:
            user = collection.find({'username': user_username})
            timestamp = str(datetime.datetime.utcnow())
            if len(list(user)) == 1:
                userUpd = collection.update({'username': user_username}, {'$push': {'tokens': [token_amount, description, timestamp]}})
                return 'tokens added at' + timestamp + 'with desc :' + description
            else:
                return 'user not found'
        except Exception as e:
            return str(e)

    def get_won_money():
        database = Database.connectDB()
        collection = database['user']
        try:
            result = collection.find()
            return result
        except Exception as e:
            return str(e)

    def add_model(user_username, model):
        database = Database.connectDB()
        userCollection = database['user']
        modelCollection = database['model']
        try:
            modelID = str(uuid.uuid4())
            timestamp = str(datetime.datetime.utcnow())
            newModel = modelCollection.insert({'ids': modelID, 'model': model})
            user = userCollection.update({'username': user_username}, {'$push': {'models': [modelID, timestamp]}})
        except Exception as e:
            return str(e)

    def add_model_from_vehicule(model, user_username):
        database = Database.connectDB()
        collection = database['model']
        try:
            save = collection.insert({'model': model, 'username': user_username})
            return True
        except Exception as e:
            return str(e)

    def checkUser(username, password):
        database = Database.connectDB()
        collection = database['user']
        try:
            result = collection.find({'username': username, 'password': password})
            if len(list(result)) == 1:
                return True
            else:
                return False
        except Exception as e:
            return str(e)

    def saveNewUser(infos):
        database = Database.connectDB()
        collection = database['user']
        try:
            exist = collection.find({'username': infos['username']})
            if len(list(exist)) == 0:
                save = collection.insert({'ids': str(uuid.uuid4()), 'username': infos['username'], 'password': infos['password'], 'email': infos['email']})
                return True
            else:
                return False
        except Exception as e:
            return str(e)


class VehiculeDB:

    def saveNewVehicule(infos):
        database = Database.connectDB()
        userCollection = database['user']
        vehiculeCollection = database['vehicule']
        try:
            vehiculeID = uuid.uuid4()
            exist = vehiculeCollection.find({'id': vehiculeID})
            userExist = userCollection.find({'username': infos['username']})
            if len(list(exist)) == 0 and len(list(userExist)) == 1:
                save = vehiculeCollection.insert({'username': infos['username'], 'id': infos['id']})
                return vehiculeID
            else:
                return None
        except Exception as e:
            return str(e)


class ContestDB:

    def get_all_contests():
        database = Database.connectDB()
        collection = database['contest']
        try:
            contests = collection.find()
            return dumps(contests)
        except Exception as e:
            return str(e)