from pymongo import MongoClient
import uuid

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

    def assign_vehicule_to_user(user_username, vehicule_id):
        database = Database.connectDB()
        userCollection = database['user']
        vehiculeCollection = database['vehicule']
        try:
            user = userCollection.find({'username': user_username})
            vehicule = vehiculeCollection.find({'id': vehicule_id})
            if len(list(user)) == 1 and len(list(vehicule)) == 1:
                userCollection.update({'username' :user_username}, {'$set' : {'vehicule_id': vehicule_id}})
                return 'checked'
            else:
                return 'either no user or no vehicule matched'
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
            contest_id = str(uuid.uuid4())
            userCollection = database['user']
            contestCollection = database['contest']
            user = userCollection.find({'username': user_username})
            if infos['name'] is None:
                return 'need a name please'
            elif infos['started_at'] is None:
                return 'need a started'
            if len(list(user)) == 1:
                save = contestCollection.insert({'ids': contest_id, 'name': infos['name'], 'starts_at': infos['starts_at']})
                userUpd = userCollection.update({'username' :user_username}, {'$push' : {'contest_id': contest_id}})
                return 'Contest created'
            else:
                return 'no user found'
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
                result = collection.find({'email': username, 'password': password})
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
            exist = vehiculeCollection.find({'id': infos['id']})
            userExist = userCollection.find({'username': infos['username']})
            if len(list(exist)) == 0 and len(list(userExist)) == 1:
                save = vehiculeCollection.insert({'username': infos['username'], 'id': infos['id']})
                return True
            else:
                return False
        except Exception as e:
            return str(e)


class ContestDB:

    def get_all_contests():
        database = Database.connectDB()
        collection = database['contest']
        try:
            contests = collection.find()
            return list(contests)
        except Exception as e:
            return str(e)