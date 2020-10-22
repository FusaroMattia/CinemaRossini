from flask import Blueprint, render_template, redirect, url_for, request,flash,session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, AnonymousUserMixin
from . import db
from sqlalchemy import create_engine, text
from flask_user import login_required,UserManager, UserMixin, SQLAlchemyAdapter,roles_required
import sqlite3

client = Blueprint('client', __name__)
engine = create_engine("postgresql+psycopg2://cliente:1234@localhost/rossini")


@client.route('/choosesit',  methods=['POST'])
#@roles_required('Cliente')
def choosesit():
    if request.method == "POST" :
       id_proiezione = request.form.get('proiezione')

       conn = engine.connect()
       trans = conn.begin()
       try:
           query = "SELECT * FROM proiezioni WHERE idproiezione ="+str(id_proiezione)
           result = conn.execute(query)
           pro_row = result.fetchone()
           posti_liberi = pro_row[5]
           posti_occupati = pro_row[6]

           query = "SELECT * FROM acquisti WHERE proiezione ="+str(id_proiezione)
           posti = conn.execute(query)
           lista_posti_occupati = []
           for row in posti:
               local_posti_occupati = row[3]
               lista_posti_occupati.extend(local_posti_occupati)

           trans.commit()
       except:
              trans.rollback()
              print("rollback")
    return 0
