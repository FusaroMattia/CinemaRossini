# -*- coding: UTF-8 -*-
from flask_login import UserMixin,AnonymousUserMixin
from flask_user import UserMixin
from . import db

# la classe user per sqlalchemy
# usata per autenticare l'utente e riconscere il suo ruolo
class User(UserMixin, db.Model):
    __tablename__ = "utenti"
    __table_args__ = {'extend_existing': True}  #estende la tabella gia presente nel db
    id = db.Column(db.Integer, primary_key=True) # Chiave primaria richiesta da sqlalchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(100))

    gestore = db.Column(db.Integer)

    cognome = db.Column(db.String(100))
    citta = db.Column(db.String(100))
    stato = db.Column(db.String(100))
    data_nascita = db.Column(db.Date)
    sesso = db.Column(db.String(10))
    riduzione = db.Column(db.Integer)


    def __init__(self, email, name, password,cognome,citta,stato,data_nascita,sesso,riduzione,     gestore):
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
