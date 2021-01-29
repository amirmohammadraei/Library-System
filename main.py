from os import execle
import re
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
        message = None    
        userDetails = request.form
        username = userDetails['username']
        password = userDetails['password']
        h = hashlib.md5(password.encode())
        cur = mysql.connection.cursor()
        resultValue = cur.execute(f"SELECT * from user_account where username = '{username}' and password = '{password}'")
        userDetail = cur.fetchall()
        try:
            userDetail[0]
            global nameprof
            global userid
            nameprof = userDetail[0][1]
            userid = userDetail[0][0]
            print(f"---------------------------------------------------{type(userid)}-------------------------------")
            print(nameprof)
            return redirect('/profile')
        except IndexError as e:
            print(e)
            message = "Invalid username or password"
        return render_template('login.html', message=message)
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
    return render_template('sprofile.html', nameprof=nameprof)


@app.route('/informations', methods=['GET', 'POST'])
def informations():
    cur = mysql.connect.cursor()
    sql = "SELECT user_account.username, user_information.fname, user_information.surname, user_information.address, user_information.role \
            FROM user_account INNER JOIN user_information ON user_information.userid = user_account.userid \
            where user_account.userid = %s"
    cur.execute(sql, str(userid))
    res = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    username = res[0][0]
    fname = res[0][1]
    surname = res[0][2]
    address = res[0][4]
    role = res[0][3]
    print(res[0])
    return render_template("information.html", username=username, fname=fname, surname=surname, address=address, role=role)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        details = request.form
        name = details['name']
        write = details['writer']
        date = details['date']
        password = details['password']
        sql = "select * from book where %s is not null and %s is not null and %s is no"
        cur = mysql.connect.cursor()
        cur.execute(sql, [name])
        x = cur.fetchall()
        print(f"------------------------------{x}")
        return render_template('search.html')
    return render_template('search.html')


@app.route('/search', methods=['GET', 'POST'])
def get_book():
    return