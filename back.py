from flask import Flask, render_template,request, redirect
from flask import session
import pymysql as sql
import random as rd

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

@app.route('/signup')
def signup():
    return render_template("signup_06.html")

if __name__ == '__main__':
    app.run(debug=True)
