from flask import Blueprint, render_template, request, flash, redirect, url_for
from client.database import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user, LoginManager

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password = request.form.get('password')
        rewritePassword = request.form.get('passwordRewrite')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 1:
            flash('Email must not be empty.', category='error')
        elif len(firstName) < 1:
            flash('First name must not be empty.', category='error')
        elif len(password) < 1:
            flash('Password must not be empty.', category='error')
        elif password != rewritePassword:
            flash('Passwords do not match.', category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(password, method='pbkdf2:sha256'), first_name=firstName)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))
    return render_template("signup.html", user=current_user)
