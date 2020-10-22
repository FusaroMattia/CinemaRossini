from flask_login import UserMixin,AnonymousUserMixin
from flask_user import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = "utenti"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(100))

    gestore = db.Column(db.Integer,db.ForeignKey('ruoli.id', ondelete='RESTRICT'), server_default='2')

    cognome = db.Column(db.String(100))
    citta = db.Column(db.String(100))
    stato = db.Column(db.String(100))
    data_nascita = db.Column(db.Date)
    sesso = db.Column(db.String(10))
    riduzione = db.Column(db.Integer)


    def __init__(self, email, name, password,cognome,citta,stato,data_nascita,sesso,riduzione,gestore):
            self.name = name
            self.email = email
            self.password = password
            self.cognome = cognome
            self.citta = citta
            self.stato = stato
            self.data_nascita = data_nascita
            self.sesso = sesso
            self.riduzione = riduzione
            self.gestore = gestore


class Role(db.Model):
    __tablename__ = "ruoli"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
