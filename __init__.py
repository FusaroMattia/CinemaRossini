
# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, url_for,request,g, request,Blueprint
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
db = SQLAlchemy()

# PAGINA DI CARICAMENTO INZIALE
# CONTIENE TUTTE LE PREFERENZE, VARIABILI ED INIZIALIZZAZIONI DEL MIO PROGETTO

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://admin:admin@localhost/rossini'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    app.config["CSRF_ENABLED"]=True
    app.config["USER_ENABLE_EMAIL"]=False               # posso anche non certificarmi via email
    app.config['SECRET_KEY'] = "1234"                   # chiave di sicurezza
    app.config['USER_LOGIN_TEMPLATE'] = 'login.html'     #pagina dove veniamo reinerizzati se non siamo loggati

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.session_protection = "strong"
    login_manager.init_app(app)

    from .models import User      #importo il modello User per il mio auth.py


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    #seguono tutte le pagine del progetto caricate da blueprint

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .manager import manager as manager_blueprint
    app.register_blueprint(manager_blueprint)

    from .client import client as client_blueprint
    app.register_blueprint(client_blueprint)

    return app
