from flask import Flask, request, make_response, jsonify
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from db import User, Vehicule, Model, Wallet, Contest, Race, Stat
import uuid
import jwt
import datetime

app = Flask(__name__)

# configure db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chainrace.db'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = ''

db = SQLAlchemy(app)


mysql = MySQL(app)

#jwt related
app.config['SECRET_KEY'] = 'thatsasecret'

def token_required(f):
    # @wraps(f)
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
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users(ids, username, email, password) VALUES (%s, %s, %s, %s)", (public_id, username, email, hashed_password))
    mysql.connection.commit()
    cur.close()
    return 'registered succesfuly'

# login senseY etre fonctionnel
@app.route('/login', methods=['POST'])
def login():
    auth = request.form
    cur = mysql.connection.cursor()
    user = cur.execute("SELECT * FROM users where username=" + auth.get('username'))
    mysql.connection.commit()
    cur.close()
    if user is None:
        return jsonify({'message' : 'invalid username'})
    else if not check_password_hash(user.get('hash_password'), auth.get('password'))
        return jsonify({'message' : 'invalid password'})
    else 
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
        return jsonify('message': 'user not found')
    return jsonify('user': user)

# route senseY etre fonctionnelle
@app.route('/users/delete/<public_id>', methods=['DELETE'])
@token_required
def delete_one_user(current_user, public_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users where ids=" + public_id)
    user = cur.fetchone()
    if not user:
        return jsonify('message': 'user not found')
    cur.execute("DELETE FROM users where ids=" + public_id)
    mysql.connection.commit()
    cur.close()
    return jsonify('message': 'user deleted')


@app.route('/vehicule/claim/<userid>', methods=['POST'])
@token_required
def claim_vehicule(current_user, userid):
    return ''



if __name__ == '__main__':
    app.run(debug=True)




# class Database:
#     def __init__(self):
#         host = "127.0.0.1"
#         user = "test"
#         password = "password"
#         db = "employees"
#         self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
#                                    DictCursor)
#         self.cur = self.con.cursor()

#     def list_employees(self):
#         self.cur.execute("SELECT first_name, last_name, gender FROM employees LIMIT 50")
#         result = self.cur.fetchall()
#         return result