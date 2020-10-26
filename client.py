from flask import Blueprint, render_template, redirect, url_for, request,flash,session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, AnonymousUserMixin
from . import db
from sqlalchemy import create_engine, text
import sqlite3

client = Blueprint('client', __name__)
engine = create_engine("postgresql+psycopg2://cliente:ciao@localhost/rossini")


@client.route('/choosesit',  methods=['POST'])
def choosesit():
    if current_user.gestore == 0 and request.method == "POST" :
       id_proiezione = request.form.get('proiezione')
       lista_posti_occupati = 0;
       conn = engine.connect()
       trans = conn.begin()
       try:

           query_proiezioni = "SELECT * FROM proiezioni WHERE idproiezione ="+str(id_proiezione)
           risultato = conn.execute(query_proiezioni)
           record_proiezione = risultato.fetchone()

           posti_liberi = record_proiezione[5]
           posti_occupati = record_proiezione[6]


           query_acquisti = "SELECT * FROM acquisti WHERE proiezione ="+str(id_proiezione)
           records_posti = conn.execute(query_acquisti)
           num_record = records_posti.rowcount

           if int(num_record) == 0:
               lista_posti_occupati = 0
           else:
               lista_posti_occupati = []
               for row in records_posti:
                   lista_posti_occupati.extend( [ row[3] ])
           trans.commit()
       except:
              trans.rollback()
              print("rollback choose sit")
       finally:
           conn.close()
           return render_template('choosesit.html',posti_occupati=lista_posti_occupati,liberi=posti_liberi,occupati=posti_occupati,proiezione=id_proiezione)
    else:
        return redirect(url_for('main.index'))

@client.route('/booking',  methods=['POST'])
def booking():
    if current_user.gestore == 0 and request.method == "POST" :
       posti_tot = int(request.form.get('postitot'))
       id_proiezione = request.form.get('proiezione')
       conn = engine.connect()
       trans = conn.begin()
       try:
           for x in range(1, posti_tot + 1 ):
               string_posto_request = "posto"+str(x)
               posto_request= request.form.get(string_posto_request)
               id_utente = current_user.get_id()
               if posto_request and posto_request != 0 :
                   query_insert_acquisti = "INSERT INTO acquisti(utente,proiezione,posti) VALUES('"+ str(id_utente) +"','"+ str(id_proiezione) +"', '"+ str(posto_request) +"') "
                   conn.execute(query_insert_acquisti)

                   query_update_proiezioni = "UPDATE proiezioni SET posti_liberi = posti_liberi-1, posti_occupati = posti_occupati+1  WHERE idproiezione ="+str(id_proiezione)
                   conn.execute(query_update_proiezioni)

           trans.commit()
       except Exception as e:
           print(e)
           trans.rollback()
           print("rollback booking")
       finally:
           conn.close()
           return render_template('booking.html')
    else:
        return redirect(url_for('main.index'))




@client.route('/allbook')
@login_required
def allbook():
    if current_user.gestore == 0 :
        id = current_user.get_id()
        proiezioni = []
        conn = engine.connect()
        trans = conn.begin()

        try:
            query_acquisti = "SELECT s.nome, f.titolo, p.data, p.ora, a.posti,a.id FROM acquisti a JOIN proiezioni p ON(a.proiezione =  p.idproiezione) JOIN sale s ON(p.sala = s.nsala) JOIN film f ON(p.film = f.codfilm) WHERE a.utente = "+str(id)
            result = conn.execute(query_acquisti)
            for n in result:
                local = [n[0],n[1],n[2],n[3],n[4],n[5]]
                proiezioni.append(local)
            trans.commit()
        except:
            trans.rollback()
            print("rollback allbook")
        finally:
            conn.close()
            return render_template('allbook.html',proiezioni = proiezioni )
    else:
        return redirect(url_for('main.index'))
