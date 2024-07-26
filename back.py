from flask import *
import pymysql as sql
from flask import session
from getpass import getpass
import math
import random
import smtplib
import bcrypt



app = Flask(__name__)

app.secret_key = 'ferhgeoriugheoighelgng45546rherojheg@'

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
    
def connect():
    db = sql.connect(host='localhost', port=3306, user='root', password='', database='calmai')
    cur = db.cursor(sql.cursors.DictCursor)
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

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')

        db, cur = connect()
        try:
            # Execute SQL query with parameters
            cur.execute(f"SELECT user_id, username, email, phone FROM users WHERE email = '{email}' and password_hash = '{password}';")
            data = cur.fetchone()

            if data:
                # Check if the entered password matches the stored hashed password
                if bcrypt.checkpw(password.encode('utf-8'), data['password_hash'].encode('utf-8')):
                    session['user'] = data['username']  # Store username in session
                    return redirect('/')
                else:
                    print("Password does not match")
            else:
                print("Email not found")
        except Exception as e:
            print(f"Database error: {e}")
        finally:
            db.close()  # Close the database connection

        return render_template("login_06.html", message="Invalid Credentials")

    return render_template('login_06.html')

@app.route("/reset")
def reset():
    return render_template("reset_07.html")

@app.route('/signup', methods=['GET','POST'])
def signup():
    return render_template("signup_06.html")

@app.route("/aftersubmit", methods=['GET', 'POST'])
def aftersubmit():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        digits = '0123456789'
        ca_id = digits[math.floor(random.random()*10)]
        name = request.form.get("name")
        email = request.form.get("email")
        password_hs = request.form.get("password")
        # password_hs = hash_password(password)
        phone = request.form.get("phone")

        db, cur = connect()
        if passkey(password_hs):
            query = "INSERT INTO users (user_id, username, email, password_hash, phone) VALUES (%s, %s, %s, %s, %s)"
            values = (ca_id, name, email, password_hs, phone)
        else:
            return render_template("signup_06.html", message = "Password is not Right")
        try:
            cur.execute(query, values)
            db.commit()
        except sql.MySQLError as e:
            print(f"Error: {e}")
            db.rollback()  # Roll back the transaction in case of error
        
        # cmd1 = f"select user_id,username,email,phone from users where email = '{email}' and  password_hash = '{password_hs}';"
        # cur.execute(cmd1)
        # data = cur.fetchone()
        # session['user'] = data
        return render_template("index_01.html", message = "User successfully registered")

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
