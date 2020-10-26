from flask import Blueprint, render_template, redirect, url_for, request,flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, AnonymousUserMixin
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
     if request.method == "POST" :
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user or not (user.password == password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))
     else:
        if current_user.is_authenticated :
            flash( "Alredy Logged in")
            return redirect(url_for("main.profile"))
        else:
            flash( "ERRORE")
            return redirect(url_for("auth.login"))


@auth.route('/login')
def login_post():
    if current_user.is_authenticated :
        flash( "Alredy Logged in")
        return redirect(url_for("main.profile"))
    else:
        return render_template('login.html')




@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    #RESTO
    cognome = request.form.get('cognome')
    citta = request.form.get('citta')
    stato = request.form.get('stato')
    data = request.form.get('data_nascita')
    sesso = request.form.get('sesso')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))


    new_user = User(email=email, name=name, password=password,cognome=cognome, citta=citta, stato=stato, data_nascita=data,sesso=sesso,riduzione="0", gestore = "0")
    #new_user.roles = [Role(id='3',name='Cliente')]
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))




@auth.route('/signup')
def signup():
    if current_user.is_authenticated :
        flash( "Alredy Logged in")
        return redirect(url_for("main.profile"))
    else:
        return render_template('singup.html')

@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))
