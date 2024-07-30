from flask import Flask, render_template, redirect, request, session
from flask_session import Session
import random as rd
import math
import pymysql as sql


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def conn():
    db = sql.connect(host='localhost', user='root', password='', database='calmai')
    cur = db.cursor()
    return db,cur 

def passkey(password):
        
    lower= 0
    upper=0
    special = 0
    digit = 0
    
    for char in password:
        if char.isdigit():
            digit += 1
        elif char.isupper():
            upper += 1
        elif char.islower():
            lower += 1
        elif not char.isidentifier():
            special += 1
        
    if lower>=1 and upper>=1 and digit>=1 and special>=1 and len(password)>=8:
        return True
    else:
        return False
    

@app.route('/')
def home():
    if 'email' not in session:
        return render_template('login_06.html')
    return render_template('index_01.html')

@app.route('/services/')
def service():
    return render_template('services_03.html')

@app.route('/about/')
def about():
    return render_template('about_02.html')

@app.route('/contact')
def contact():
    return render_template('contact_05.html')

@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db,cur = conn()
        try:
            cmd = f"SELECT username,email,phone FROM users where email ='{email}' and password_hash = '{password}';"
            cur.execute(cmd)
            data = cur.fetchone()
            if data:
                session['name'] = data[0]
                session['email'] = data[1]
                return redirect('/')
            else:
                print('Details does not match')
        except Exception as e:
            print(e)
            return render_template('login_06.html', message = 'Invalid Credentials')
    return render_template('login_06.html')
@app.route('/signup/')
def signup():
    return render_template('signup_06.html')

@app.route('/aftersubmit/', methods=['GET','POST'])
def aftersubmit():
    if request.method == 'POST':
        digits = '0123456789'
        id = math.floor(rd.random()*1000000)
        name = request.form.get('name')
        session['name'] = name
        email = request.form.get('email')
        session['email'] = email
        phone = request.form.get('phone')
        password = request.form.get('password')
        db,cur = conn()
        if passkey(password):
            cur.execute(f"INSERT INTO users (user_id,username,email,password_hash,phone) VALUES ({id},'{name}','{email}','{password}','{phone}');")
            db.commit()
            return redirect('/')
        else:
            return render_template('signup_06.html', message = 'Invalid details Try Again')
        

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)