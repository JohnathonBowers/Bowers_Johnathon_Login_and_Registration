from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return redirect ('/login')

@app.route('/login')
def r_login_registration():
    return render_template('login_registration.html')

# @app.route('/register', methods='POST')
# def f_register():