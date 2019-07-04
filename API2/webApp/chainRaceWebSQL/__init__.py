from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# configure db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/ChainRaceDB'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'ChainRaceDB'

db = SQLAlchemy(app)

#jwt related
app.config['SECRET_KEY'] = 'thatsasecret'

from chainRaceWeb import routes