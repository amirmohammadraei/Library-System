from flask import Flask, render_template, redirect, request
import yaml
from flask_mysqldb import MySQL


app = Flask(__name__)


db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userDetails = request.form
        username = userDetails['username']
        user_password = userDetails['password']
        cur = mysql.connection.cursor()
        resultValue = cur.execute(f"SELECT * from user_account where username = '{username}'")
        userDetail = cur.fetchall()
        print(userDetail)
        return 'salam'
    return render_template('login.html')












"""
import hashlib
password = 'pa$$w0rd'
password1 = 'pa$$w0rd'
h = hashlib.md5(password.encode())
j = hashlib.md5(password1.encode())
print(h.hexdigest())
print(j.hexdigest())from """