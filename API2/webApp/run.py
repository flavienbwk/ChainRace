from chainRaceWeb import app

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