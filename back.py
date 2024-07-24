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
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

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

@app.route('/login')
def login():
    return render_template("login_06.html")

@app.route("/reset")
def reset():
    return render_template("reset_06.html")

@app.route('/signup', methods=['GET','POST'])
def signup():
    return render_template("signup_06.html")

@app.route("/aftersubmit", methods = ['GET','POST'])
def aftersubmit():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        ca_id = random.randrange(1,1000)

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        password_hs = hash_password(password)
        phone = request.form.get("phone")
        db,cur = connect()
        cur.execute(f"INSERT INTO users VALUES({ca_id},'{name}','{email}','{password_hs}','{phone}')")
        db.commit()

        cmd1 = f"select ca_name,ca_email,ca_phn from users where email = '{email} and  password_hashed = '{password_hs};"
        cur.execute(cmd1)
        data = cur.fetchone()
        session['user'] = data
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
