from flask import Flask, render_template
app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')











"""
import hashlib
password = 'pa$$w0rd'
password1 = 'pa$$w0rd'
h = hashlib.md5(password.encode())
j = hashlib.md5(password1.encode())
print(h.hexdigest())
print(j.hexdigest())from """