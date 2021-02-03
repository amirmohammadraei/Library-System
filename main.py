from os import error, execle, write
import re
from typing import Counter
import MySQLdb
from flask import Flask, render_template, redirect, request, redirect, url_for
from flask.helpers import flash
from werkzeug import datastructures
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
            global user_role
            nameprof = userDetail[0][1]
            userid = userDetail[0][0]
            user_role = userDetail[0][3]

            if userDetail[0][3] == 'manager':
                return redirect('/manager')

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
    cur.execute(sql, [userid])
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
        version = details['version']
        cur = mysql.connect.cursor()
        try:
            if name != "" and write == "" and date == "" and version == "":
                sql = "select bookid, name, writer, types, date, verion from book where name = %s order by name"
                cur.execute(sql, [name])
            if name == "" and write != "" and date == "" and version == "":
                sql = "select bookid, name, writer, types, date, verion from book where writer = %s order by name"
                cur.execute(sql, [write])
            if name == "" and write == "" and date != "" and version == "":
                sql = "select bookid, name, writer, types, date, verion from book where date = %s order by name"
                cur.execute(sql, [date])
            if name == "" and write == "" and date == "" and version != "":
                sql = "select bookid, name, writer, types, date, verion from book where verion = %s order by name"
                cur.execute(sql, [version])

            if name != "" and write != "" and date == "" and version == "":
                sql = "select bookid, name, writer, types, date, verion from book where name = %s and writer = %s order by name"
                cur.execute(sql, [name, write])
            if name != "" and write == "" and date != "" and version == "":
                sql = "select bookid, name, writer, types, date, verion from book where name = %s and date = %s order by name"
                cur.execute(sql, [name, date])
            if name != "" and write == "" and date == "" and version != "":
                sql = "select bookid, name, writer, types, date, verion from book where verion = %s and name = %s order by name"
                cur.execute(sql, [version, name])
            if name == "" and write != "" and date != "" and version == "":
                sql = "select bookid, name, writer, types, date, verion from book where writer = %s and date = %s order by name"
                cur.execute(sql, [write, date])
            if name == "" and write != "" and date == "" and version != "":
                sql = "select bookid, name, writer, types, date, verion from book where verion = %s and writer = %s order by name"
                cur.execute(sql, [version, write])
            if name == "" and write == "" and date != "" and version != "":
                sql = "select bookid, name, writer, types, date, verion from book where verion = %s and date = %s order by name"
                cur.execute(sql, [version, date])

            if name != "" and write != "" and date != "" and version == "":
                sql = "select bookid, name, writer, types, date, verion from book where name = %s and writer = %s and date = %s order by name"
                cur.execute(sql, [name, write, date])
            if name != "" and write != "" and date == "" and version != "":
                sql = "select bookid, name, writer, types, date, verion from book where name = %s and writer = %s and verion = %s order by name"
                cur.execute(sql, [name, write, version])
            if name != "" and write == "" and date != "" and version != "":
                sql = "select bookid, name, writer, types, date, verion from book where name = %s and verion = %s and date = %s order by name"
                cur.execute(sql, [name, version, date])
            if name == "" and write != "" and date != "" and version != "":
                sql = "select bookid, name, writer, types, date, verion from book where verion = %s and date = %s and writer = %s order by name"
                cur.execute(sql, [version, date, write])

            if name != "" and write != "" and date != "" and version != "":
                sql = "select bookid, name, writer, types, date, verion from book where name = %s and verion = %s and date = %s and writer = %s order by name"
                cur.execute(sql, [name, version, date, write])
        except MySQLdb.OperationalError as e:
            print(e)
            return render_template('search.html', message="Please enter valid format for date field")
        try:
            x = cur.fetchall()
            x[0][0]
            mysql.connection.commit()
            cur.close()
        except:
            return render_template('search.html')
        print('----------------')
        print(x)
        print('----------------')
        return render_template('reserve.html', data=x)

    return render_template('search.html')


@app.route('/reserve', methods=['GET', 'POST'])
def get_book():
    if request.method == 'POST':
        details = request.form['reserve']
        dbb = MySQLdb.connect(host="localhost", 
        user="root", 
        passwd="root", 
        db="dbproject")
        curb = dbb.cursor()
        curb.execute("select * from book where bookid = %s", [details])
        res = curb.fetchall()
        curb.execute("select delay from user_account where userid = %s", [userid])
        userdelay = curb.fetchone()


        try:
            curb.execute("update user_account u join book b set u.money = u.money - ( b.price * 5 ) / 100 where u.userid = %s and b.bookid = %s", [userid, details])
        except MySQLdb.OperationalError:
            message = "کتابی با چنین شناسه‌ای در کتابخانه موجود نیست"
            res = curb.execute("insert into getbook_opt(message, operation, userid) values (%s, %s, %s)", [message, False, userid])
            dbb.commit()
            return render_template('getbook.html', message=message)
        except Exception as e:
            message = "موجودی کافی نیست"
            res = curb.execute("insert into getbook_opt(message, operation, userid) values (%s, %s, %s)", [message, False, userid])
            dbb.commit()
            return render_template('getbook.html', message=message)


        if userdelay[0] == 4:
            curb.close()
            message = "به دلیل ۴ بار دیر کرد در تحویل کتاب در بازه ۲ ماه اخیر، اجازه گرفتن کتاب را ندارید"
            res = curb.execute("insert into getbook_opt(message, operation, userid) values (%s, %s, %s)", [message, False, userid])
            dbb.commit()
            return render_template('getbook.html', message=message)

        try:
            print(res[0])
            curb.execute("UPDATE BOOK SET count = count + %s where bookid = %s", [-1, details])


            if user_role == 'student':
                curb.execute("select * from user_account u join book b where u.role = %s and (b.types = '' or b.types = 'amoozeshi') and u.userid = %s and b.bookid = %s;", [user_role, userid, details])
                res = curb.fetchall()
                try:
                    res[0]
                except IndexError:
                    message = "شما مجاز به گرفتن این کتاب نیستید"
                    res = curb.execute("insert into getbook_opt(message, operation, userid) values (%s, %s, %s)", [message, False, userid])
                    # dbb.commit()
                    return render_template('getbook.html', message=message)
            
            if user_role == 'guser':
                curb.execute("select * from user_account u join book b where u.role = %s and b.types = '' and u.userid = %s and b.bookid = %s;", [user_role, userid, details])
                res = curb.fetchall()
                try:
                    res[0]
                except IndexError:
                    message = "شما مجاز به گرفتن این کتاب نیستید"
                    res = curb.execute("insert into getbook_opt(message, operation, userid) values (%s, %s, %s)", [message, False, userid])
                    dbb.commit()
                    curb.close()
                    return render_template('getbook.html', message=message)


            dbb.commit()
            res = curb.fetchall()
            message = "کتاب با موفقیت به حساب شما اضافه شد"
            res = curb.execute("insert into getbook_opt(message, operation, userid) values (%s, %s, %s)", [message, True, userid])
            message2 = "را به صورت موفقیت آمیز درخواست داده است"
            res = curb.execute("insert into inbox(message, operation, userid, bookid) values (%s, %s, %s, %s)", [message2, True, userid, details])
            dbb.commit()
            return render_template('getbook.html', messages=message)
        except IndexError:
            message = "کتابی با چنین شناسه‌ای در کتابخانه موجود نیست"
            res = curb.execute("insert into getbook_opt(message, operation, userid) values (%s, %s, %s)", [message, False, userid])
            dbb.commit()
            return render_template('getbook.html', message=message)
        except MySQLdb.OperationalError:
            message = "کتاب درخواستی در حال حاضر موجود نیست"
            res = curb.execute("insert into getbook_opt(message, operation, userid) values (%s, %s, %s)", [message, False, userid])
            dbb.commit()
            return render_template('getbook.html', message=message)
        return render_template('getbook.html')
    return render_template('getbook.html')


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        money = request.form['payment']
        dbb = MySQLdb.connect(host="localhost", 
        user="root", 
        passwd="root", 
        db="dbproject")
        curb = dbb.cursor()
        try:
            curb.execute ("UPDATE user_account SET money = money + %s WHERE userid = %s;", [money, userid])
            dbb.commit()
        except MySQLdb.OperationalError as e:
            message = e.args[1]
            if 'Truncated' in message:
                message = "مبلغ وارد شده باید به صورت عددی باشد"
            curb.execute("select money from user_account where userid = %s", [userid])
            res = curb.fetchall()
            mysql.connection.commit()
            curb.close()
            return render_template('payment.html', money=res[0][0], message=message)
        except:
                message = "مبلغ وارد شده باید به صورت عددی و معقول باشد"
                curb.execute("select money from user_account where userid = %s", [userid])
                res = curb.fetchall()
                return render_template('payment.html', money=res[0][0], message=message)
        curb.execute("select money from user_account where userid = %s", [userid])  
        res = curb.fetchall()
        curb.close()
        return render_template('payment.html', messages= "You successfully charge your account!", money=res[0][0])
    else:
        cur = mysql.connect.cursor()
        cur.execute("select money from user_account where userid = %s", [userid])
        res = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return render_template('payment.html', money=res[0][0])


@app.route('/manager', methods=['GET', 'POST'])
def manager():
    return render_template('manager.html', nameprof=nameprof)


@app.route('/addbook', methods=['GET', 'POST'])
def addbook():
    if request.method == 'POST':
        detail = request.form
        bookname = detail['name']
        date = detail['date']
        version = detail['version']
        type = detail['type']
        writer = detail['writer']
        count = detail['count']
        dbb = MySQLdb.connect(host="localhost", 
        user="root", 
        passwd="root", 
        db="dbproject")
        curb = dbb.cursor()
        try:
            curb.execute("insert into book(name, writer, date, verion, count, types) values (%s, %s, %s, %s, %s, %s)", [bookname, writer, date, version, count, type])
            dbb.commit()
        except MySQLdb.OperationalError: 
            message = "فرمت تاریخ باید به صورت 12-12-1399 باشد"
            return render_template('addbook.html', message=message)
    return render_template('addbook.html', nameprof=nameprof)


@app.route('/inboxuser', methods=['GET', 'POST'])
def inboxuser():
    dbb = MySQLdb.connect(host="localhost", 
        user="root", 
        passwd="root", 
        db="dbproject")
    curb = dbb.cursor()
    curb.execute("select inbox.inboxid, book.name from book join inbox where book.bookid = inbox.bookid and inbox.userid = %s;", [userid])
    res = curb.fetchall()
    print(res)
    return render_template("inbox.html", data = res)


@app.route('/givebook', methods=['GET', 'POST'])
def givebook():
    return 'salam'