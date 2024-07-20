from flask import Flask, render_template,request, redirect
import pymysql as sql
from flask import session
from getpass import getpass
import math
import random
import smtplib

app = Flask(__name__)

def connect():
    db = sql.connect(host='localhost', port=3306, user='root', password='', database='calmai')
    cur = db.cursor()
    return db,cur

@app.route('/')
def home():
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
    ca_id = random.randrange(1,1000)

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    phone = request.form.get("phone")
    db,cur = connect()
    cur.execute(f"INSERT INTO userdetail VALUES({ca_id},'{name}','{email}','{password}','{phone}')")
    db.commit()

    return render_template("signup_06.html")

if __name__ == '__main__':
    app.run(debug=True)
