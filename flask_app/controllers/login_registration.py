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
        return redirect('/')
    data = {'email': request.form['email']}
    user_in_db = User.get_by_email(data)
    if user_in_db:
        flash('This email is already associated with an account. Please try logging in with this email or creating an account with a different email.')
        return redirect('/')
    if not user_in_db:
        if session:
            session.pop('first_name')
            session.pop('last_name')
            session.pop('email')
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': pw_hash
        }
        user_id = User.save(data)
        session['user_id': user_id]
        return redirect ('/dashboard')

@app.route('/dashboard')
def r_dashboard():
    if session:
        user = User.get_by_user_id(session['user_id'])
        return render_template('dashboard.html', user)
    else:
        return redirect ('/')

@app.route('/logout')
def logout():
    session.pop('first_name')
    session.pop('last_name')
    session.pop('email')
