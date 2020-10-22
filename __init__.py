from flask import Flask, render_template, redirect, url_for,request,g, request,Blueprint
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, AnonymousUserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from flask_user import login_required,UserManager, UserMixin, SQLAlchemyAdapter
#from datatime import datetime,timedelta
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://admin:admin@localhost/rossini'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    app.config["CSRF_ENABLED"]=True
    app.config["USER_ENABLE_EMAIL"]=False
    app.config['SECRET_KEY'] = "1234"

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.session_protection = "strong"
    login_manager.init_app(app)

    from .models import User

    db_adapter = SQLAlchemyAdapter(db,User)
    user_manager = UserManager(db_adapter,app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .manager import manager as manager_blueprint
    app.register_blueprint(manager_blueprint)

    from .client import client as client_blueprint
    app.register_blueprint(client_blueprint)

    return app
