from flask import Flask, render_template, redirect, request, session, flash
from flask_session import Session
import random as rd
import math
import pymysql as sql
import smtplib


app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


def conn():
    db = sql.connect(host='localhost', user='root',
                     password='', database='calmai')
    cur = db.cursor()
    return db, cur


def passkey(password):

    lower = 0
    upper = 0
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

    if lower >= 1 and upper >= 1 and digit >= 1 and special >= 1 and len(password) >= 8:
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

@app.route('/contact', methods = ['POST','GET'])
def contact():
    return render_template("contact_05.html")

@app.route("/aftercontact", methods=['GET', 'POST'])
def aftercontact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        text = request.form.get("message")
        user_id = session.get('user_id')  # Use get to avoid KeyError if 'user_id' is not in session
        
        db, cur = conn()
        try:
            cur.execute("SELECT email FROM users WHERE email = %s", (email,))
            data = cur.fetchone()
            
            if data:
                cur.execute("INSERT INTO contact (user_id, name, email, text) VALUES (%s, %s, %s, %s)", (user_id, name, email, text))
                db.commit()
                flash('Thank you for contacting us. We will get back to you shortly.')
                return redirect('/contact')
            else:
                flash("Didn't find your email, try again")
                return redirect('/signup/')
        except Exception as e:
            flash(f"An error occurred: {e}")
        finally:
            cur.close()
            db.close()
    
    return render_template('contact_05.html')

@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        db,cur = conn()
        try:
            cmd = f"SELECT user_id,username,email,phone FROM users where email ='{email}' and password_hash = '{password}';"
            cur.execute(cmd)
            data = cur.fetchone()
            if data:
                session['user_id'] = data[0]
                print(session['user_id'])
                session['name'] = data[1]
                session['email'] = data[2]
                flash('Logged in Successfully!!!')
                return render_template('index_01.html', flash=flash)
            else:
                flash('Invalid Credentials')
                return render_template('login_06.html', message = flash)
        except Exception as e:
            print(e)
            print('Details does not match')
    return render_template('login_06.html')


@app.route('/reset', methods=['GET','POST'])
def reset():
    email = request.form.get('email')
    session['email'] = email
    return render_template("reset_06.html")

@app.route('/otp', methods = ['GET','POST'])
def otp():
    db,cur = conn()

    if request.method=="GET":
        return redirect('/reset/')

    if request.method == 'POST':
       
        
    
        email = request.form.get('email')
        session['email'] = email
        digits = '0123456789'
        OTP = ''
        for i in range(6):
            OTP += digits[rd.randint(0, len(digits) - 1)]
        otp = OTP + ' is you OTP'
        msg = otp
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("itzkuldeep2002@gmail.com", "shqatengaswhpcjc")
        print(session.get('email'))
       
        s.sendmail('&&&&&&&&&&&',email,msg)
        session['otp']=OTP
        print(session['otp'])     
        return render_template("reset.html")

@app.route('/verifyotp',methods=["POST"])
def verifyotp():
    db,cur = conn()
    otp = request.form.get('otp')
    if str(otp) == str(session.get('otp')):
        print('Verified')
        new_pass = request.form.get('new_password')
        if passkey(new_pass):
            cmd1 = f"UPDATE users SET password_hash = '{new_pass}' WHERE email = '{session['email']}';"
            cur.execute(cmd1)
            db.commit()
            session['otp']=None
    
            return redirect('/')
        else:
            return {"message":"Invalid password format. Password must be at least 8 characters long and contain at least one number, one uppercase letter, one lowercase letter, and one special character"}
    else:
        return {"message":"Please Check your OTP again"}
    
    


@app.route('/signup/')
def signup():
    return render_template('signup_06.html')

@app.route('/aftersubmit/', methods=['GET','POST'])
def aftersubmit():
    if request.method == 'POST':
        digits = '0123456789'
        id = math.floor(rd.random()*1000000)
        session['user_id'] = id
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
            flash('Acoount Created Successfull!!!')
            return render_template('index_01.html', flash=flash)
        else:
            flash('Invalid details Try Again')
            return render_template('signup_06.html', message = flash)
        
@app.route('/notebook')
def notebook():
    db, cur = conn()
    id = session['user_id']
    cur.execute(f"SELECT content FROM notes WHERE user_id = {id};")
    note = cur.fetchone()  
    if note is None:
        note = []  
    print(note)
    return render_template('notebook.html', note=note)



@app.route('/add_note', methods=['POST'])
def add_note():
    note_text = request.form.get('note')
    user_id = session['user_id']
    print(session['user_id'])
    print(id)
    db,cur = conn()
    if note_text.strip() != '':
        cur.execute(f"INSERT INTO notes (user_id,content) VALUES ({user_id},'{note_text}');")
        db.commit()
    return redirect('/notebook')

@app.route('/delete_note', methods=['POST'])
def delete_note():
    db,cur = conn()
    id = session['user_id']
    cur.execute(f"DELETE FROM notes WHERE user_id = '{id}';")
    db.commit()
    return redirect('/notebook')


@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

@app.route("/blogs/")
def blogs():
    return render_template("blog_10.html")

if __name__ == '__main__':
    app.run(debug=True)
    