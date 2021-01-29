from os import execle
import MySQLdb
from flask import Flask, render_template, redirect, request, redirect
import yaml
from flask_mysqldb import MySQL
import hashlib


app = Flask(__name__)


db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)



@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':        
        userDetails = request.form
        username = userDetails['username']
        password = userDetails['password']
        h = hashlib.md5(password.encode())
        cur = mysql.connection.cursor()
        resultValue = cur.execute(f"SELECT * from user_account where username = '{username}' and password = '{password}'")
        userDetail = cur.fetchall()
        try:
            userDetail[0]
            print(userDetail[0][3])
            return 'bia too'
        except IndexError as e:
            print(e)
            return 'ridi'

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        uersDetails = request.form
        username = uersDetails['username']
        password = uersDetails['password']
        fname = uersDetails['fname']
        surname = uersDetails['surname']
        address = uersDetails['address']
        role = uersDetails['role']
        cur = mysql.connection.cursor()
        exception =None
        try:
            cur.execute("INSERT INTO user_account (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
            sql = "SELECT userid FROM user_account where username = %s"
            cur.execute(sql, [username])
            result = cur.fetchone()
            print(type(result[0]))
            print(result[0])
            cur.execute("INSERT into user_information (address, fname, surname, role, userid) VALUES (%s, %s, %s, %s, %s)", (address, fname, surname, role, result[0]))
        except MySQLdb.OperationalError as e:
            exception = e.args[1]
        except MySQLdb.IntegrityError as e:
            exception = "This username is already in use!"

        mysql.connection.commit()
        cur.close()
        if exception is not None:
            print(f"username {username}, password {password}, fname {fname}, surname {surname}, address {address}, role {role}")
            return render_template('register.html', exception=exception)
        else:
            success = "sign up successfully"
            return render_template('login.html', success=success)

    return render_template('register.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('sprofile.html')
