from flask_login import UserMixin,AnonymousUserMixin
from . import db

def __init__(self, email, name, password):
        self.name = first_name
        self.email = email
        self.password = password

class user(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
