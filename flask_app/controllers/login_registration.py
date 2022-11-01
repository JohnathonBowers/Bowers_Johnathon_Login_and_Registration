from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User

@app.route('/')
def r_login_registration():
    return render_template('login_registration.html')

@app.route('/register', methods=['POST'])
def f_register():
    if not User.validate_registration(request.form):
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['email']
        session['password'] = request.form['password']
        return redirect('/')
    data = {'email': request.form['email']}
    user_in_db = User.get_by_email(data)
    if user_in_db:
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email'] = request.form['email']
        flash('This email is already associated with an account. Please try logging in with this email or creating an account with a different email.', 'email')
        return redirect('/')
    if not user_in_db:
        if session:
            session.clear()
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': pw_hash
        }
        session['user_id'] = User.save(data)
        return redirect ('/dashboard')

@app.route('/login', methods=['POST'])
def f_login():
    data = {'email': request.form['email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        session['login_email'] = request.form['email']
        session['password'] = request.form['password']
        flash('Invalid email/password', 'login')
        return redirect ('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        session['login_email'] = request.form['email']
        session['password'] = request.form['password']
        flash('Invalid email/password', 'login')
        return redirect ('/')
    session['user_id'] = user_in_db.id
    return redirect ('/dashboard')

@app.route('/dashboard')
def r_dashboard():
    if session['user_id']:
        print (session['user_id'])
        data = {'id': session['user_id']}
        user = User.get_by_user_id(data)
        return render_template('dashboard.html', user = user)
    else:
        return redirect ('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')
