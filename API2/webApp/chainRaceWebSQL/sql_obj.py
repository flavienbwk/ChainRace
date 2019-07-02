import pymysql
from chainRaceWeb import app

db_host = app.config['MYSQL_HOST']
db_user = app.config['MYSQL_USER']
db_pass = app.config['MYSQL_PASSWORD']
db_name = app.config['MYSQL_DB']

class sql:

    def get(query, data):
        db = pymysql.connect(db_host, db_user, db_pass, db_name)
        cursor = db.cursor()
        cursor.execute(query, data)
        to_ret =  cursor.fetchall()
        cursor.close()
        db.close()
        return to_ret

    def post(query, data):
        db = pymysql.connect(db_host, db_user, db_pass, db_name)
        cursor = db.cursor()
        try:
            cursor.execute(query, data)
            db.commit()
            to_ret = True
        except:
            db.rollback()
            to_ret = False
        cursor.close()
        db.close()
        return to_ret