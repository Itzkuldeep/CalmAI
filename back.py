from flask import Flask, render_template,request, redirect
import pymysql as sql
from flask import session
from getpass import getpass
import math
import random
import smtplib
import bcrypt


app = Flask(__name__)

def connect():
    db = sql.connect(host='localhost', port=3306, user='root', password='', database='calmai')
    cur = db.cursor()
    return db,cur

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def verify_password(stored_password_hash, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password_hash)

@app.route('/')
def home():
    if session.get('user'):
        return render_template("index_01.html")
    else:
        return render_template("index_01.html")

@app.route('/about')
def about():
    return render_template("about_02.html")

@app.route('/services')
def services():
    return render_template("services_03.html")

@app.route('/contact')
def contact():
    return render_template("contact_05.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get("email")
        password = request.form.get("password")

        db, cur = connect()
        query = "SELECT password_hash FROM users WHERE email = %s"
        cur.execute(query, (email,))
        result = cur.fetchone()
        
        if result and verify_password(result[0], password):
            return "Login successful"
        else:
            return "Invalid email or password"

@app.route("/reset")
def reset():
    return render_template("reset_06.html")

@app.route('/signup', methods=['GET','POST'])
def signup():
    return render_template("signup_06.html")

@app.route("/aftersubmit", methods=['GET', 'POST'])
def aftersubmit():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        ca_id = random.randrange(1, 1000)
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        password_hs = hash_password(password)
        phone = request.form.get("phone")

        db, cur = connect()
        query = "INSERT INTO users (user_id, username, email, password_hash, phone) VALUES (%s, %s, %s, %s, %s)"
        values = (ca_id, name, email, password_hs, phone)

        try:
            cur.execute(query, values)
            db.commit()
        except sql.MySQLError as e:
            print(f"Error: {e}")
            db.rollback()  # Roll back the transaction in case of error

        # return "User successfully registered"        
        # cmd1 = f"select user_id,username,email,phone from users where email = '{email} and  password_hash = '{password_hs};"
        # cur.execute(cmd1)
        # data = cur.fetchone()
        # session['user'] = data
        return redirect("/")

@app.route('/privacy')
def privacy():
    return render_template("privacy_08.html")

@app.route('/terms')
def terms():
    return render_template("terms_07.html")

@app.route('/chatbot')
def chatbot():
    return render_template("chatbot_09.html")

if __name__ == '__main__':
    app.run(debug=True)
