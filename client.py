from flask import Blueprint, render_template, redirect, url_for, request,flash,session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, AnonymousUserMixin
from . import db
from sqlalchemy import create_engine, text
from flask_user import login_required,UserManager, UserMixin, SQLAlchemyAdapter,roles_required
import sqlite3

client = Blueprint('client', __name__)
engine = create_engine("postgresql+psycopg2://admin:admin@localhost/rossini")


@client.route('/choosesit',  methods=['POST'])
#@roles_required('Cliente')
def choosesit():
    if current_user.gestore ==0 and request.method == "POST" :
       id_proiezione = request.form.get('proiezione')
       lista_posti_occupati = 0;
       conn = engine.connect()
       trans = conn.begin()
       try:
           query = "SELECT * FROM proiezioni WHERE idproiezione ="+str(id_proiezione)
           result = conn.execute(query)
           pro_row = result.fetchone()
           posti_liberi = pro_row[5]
           posti_occupati = pro_row[6]
           print(id_proiezione)
           query = "SELECT * FROM acquisti WHERE proiezione ="+str(id_proiezione)
           posti = conn.execute(query)
           num_results = posti.rowcount
           if int(num_results) == 0:
               lista_posti_occupati = 0
           else:
               lista_posti_occupati = []
               for row in posti:
                   lista_posti_occupati.extend( [ row[3] ])
           trans.commit()
       except:
              trans.rollback()
              print("rollback choose sit")
       finally:
           conn.close()
           return render_template('choosesit.html',posti_occupati=lista_posti_occupati,liberi=posti_liberi,occupati=posti_occupati,proiezione=id_proiezione)


@client.route('/booking',  methods=['POST'])
#@roles_required('Cliente')
def booking():
    if current_user.gestore == 0 and request.method == "POST" :
       posti_tot = int(request.form.get('postitot'))
       id_proiezione = request.form.get('proiezione')
       error = "none";
       conn = engine.connect()
       trans = conn.begin()
       try:
           for x in range(1, posti_tot + 1 ):
               string = "posto"+str(x)
               posti_local = request.form.get(string)
               id = current_user.get_id()
               if posti_local and posti_local != 0 :
                    query = "INSERT INTO acquisti(utente,proiezione,posti) VALUES('"+ str(id) +"','"+ str(id_proiezione) +"', '"+ str(posti_local) +"') "
                    conn.execute(query)
                    query = "UPDATE proiezioni SET posti_liberi = posti_liberi-1, posti_occupati = posti_occupati+1  WHERE idproiezione ="+str(id_proiezione)
                    conn.execute(query)

           trans.commit()
       except:
           trans.rollback()
           print("rollback booking")
           error = "rollback"
       finally:
          conn.close()
          return render_template('booking.html',error = error)
