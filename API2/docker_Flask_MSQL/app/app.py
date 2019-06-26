from flask import Flask, request, make_response, jsonify
from flask_mysqldb import MySQL
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime

app = Flask(__name__)

# configure db
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = ''

mysql = MySQL(app)

#jwt related
app.config['SECRET_KEY'] = 'thatsasecret'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #unvalid way
        if not token:
            return jsonify({'message' : 'Token is missing'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid'}), 403

        return f(*args, **kwargs)
    return decorated


@app.route('/')
def hello_world():
    return 'Hello, World!'


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


@app.route('/login', methods=['POST'])
def login():
    auth = request.form

    if auth and auth.get('username') == 'xxkingxx' and auth.get('password') == '123456':
        token = jwt.encode({'user' : auth.get('username'), 'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})

    print(auth.get('username'))
    print(auth.get('password'))

    return make_response('could not verify', 401, {'WWW-Authenticate' : 'Basic-realm:"Login Required"'})


@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resValue = cur.execute("SELECT * FROM users")
    if resValue > 0:
        userDetails = cur.fetchall()
    return userDetails


@app.route('/<userid>/addVehicule', methods=['POST'])
def addVehicule(userid):
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