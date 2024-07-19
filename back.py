from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index_01.html")

@app.route('/about')
def about():
    return render_template("about_02.html")

@app.route('/resources')
def services():
    return render_template("resources_03.html")

@app.route('/self-assessment')
def self():
    return render_template("self_04.html")

@app.route('/contact')
def contact():
    return render_template("contact_05.html")

@app.route('/login')
def login():
    return render_template("login_06.html")

@app.route('/signup')
def signup():
    return render_template("signup_06.html")

if __name__ == '__main__':
    app.run(debug=True)
