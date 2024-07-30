from flask import *
import random as rd
import math

app = Flask(__name__)


@app.route('/')
def home():
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

@app.route('/login/')
def login():
    return render_template('login_06.html')

@app.route('/signup/')
def signup():
    return render_template('signup_06.html')

@app.route('/aftersubmit/', methods=['GET','POST'])
def aftersubmit():
    if request.method == 'POST':
        digits = '0123456789'
        id = math.floor(rd.random()*1000000)
        

if __name__ == '__main__':
    app.run(debug=True)