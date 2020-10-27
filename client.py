# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, redirect, url_for, request,flash,session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, AnonymousUserMixin
from . import db
from sqlalchemy import create_engine, text
from datetime import date, datetime

# PAGINA .PY DEDICATA AL RUOLO cliente, IN CUI HO LE ROUTE ESEGUIBILI
# mi connetto attraverso il ruolo cliente

client = Blueprint('client', __name__)
engine = create_engine("postgresql+psycopg2://cliente:ciao@localhost/rossini")


# Route che viene caricata ogni volta che clicchiamo sul tasto ACQUISTA nell'index.html o nel FILM.HTML
# Necessita di avere una variabile passata con metodo "post" e che io sia un cliente
# In base a ciò che passiamo restituirà la suddivisioni dei posti sulla sala e segnerà quelli già acquistati
# quindi nella mia pagina html avrò tutti i posti vuoti selezionabili
@client.route('/choosesit',  methods=['POST'])
def choosesit():
    if current_user.gestore == 0 and ( request.method == "POST" or request.args['proiezione']):
        if request.form.get('proiezione'):
            id_proiezione = request.form.get('proiezione')
        else:
            id_proiezione = request.args['proiezione']
        lista_posti_occupati = 0;
        conn = engine.connect()
        trans = conn.begin()
        try:
            #prende i posti liberi ed occupati in quel momento nella proiezione scelta
            query_proiezioni = "SELECT * FROM proiezioni WHERE idproiezione ="+str(id_proiezione)
            risultato = conn.execute(query_proiezioni)
            record_proiezione = risultato.fetchone()

            posti_liberi = record_proiezione[5]
            posti_occupati = record_proiezione[6]

            #prenderà tutta la lista di posti gia acquistati
            #lockando così i posti che non posso prendere
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


# Route che viene caricata ogni volta che clicchiamo sul tasto ACQUISTA I POSTI nel choosesit.html
# Necessita di avere una variabile passata con metodo "post" e che io sia un cliente
# Prova a inserire tutti i posti da noi comprati, ricordiamo che esiste il vincolo su proiezione,posti in cui non posso comprare qualcosa che è già stato prenotato
# se uno di questi risulta già comprato ci riporta a selezionare i posti, annullando l'acquisto
# aggiunge un posto occupato e toglie un posto libero in base a quanti ne abbiamo acquistati alla proiezione che il cliente vuole vedere
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
           return redirect(url_for('client.choosesit',proiezione = id_proiezione ))
       finally:
           conn.close()
           return render_template('booking.html')
    else:
        return redirect(url_for('main.index'))

# Route che viene caricata ogni volta che clicchiamo sul tasto ELIMINA nel allbook.html
# Necessita di avere una variabile passata con metodo "post" e che io sia un cliente
# Elimina la prenotazione scelta e aggiunge un posto libero e toglie un posto occupato alla proiezione
@client.route('/deletebook',methods=['POST'])
def deletebook():
    if current_user.gestore == 0 and request.method == "POST" :
        id_acquisto = int(request.form.get('acquisto'))

        conn = engine.connect()
        trans = conn.begin()
        try:
            query = "SELECT proiezione FROM acquisti WHERE id = "+str(id_acquisto)
            result = conn.execute(query)
            row = result.fetchone()
            id_proiezione = row[0]

            query = "DELETE FROM acquisti WHERE id = "+str(id_acquisto)
            conn.execute(query)

            query_update_proiezioni = "UPDATE proiezioni SET posti_liberi = posti_liberi+1, posti_occupati = posti_occupati-1  WHERE idproiezione ="+str(id_proiezione)
            conn.execute(query_update_proiezioni)
            trans.commit()
        except Exception as e:
            print(e)
            trans.rollback()
            print("rollback delete")
        finally:
            conn.close()
            return redirect(url_for('client.allbook'))

    else:
        return redirect(url_for('main.index'))

# Route che viene caricata ogni volta che clicchiamo sulla scritta PRENOTAZIONI nella NAVBAR o dopo l'acquisto
# Necessita che io sia un cliente
# Mostra a schermo tutte le prenotazioni dell'utente specificando nome sala, titolo film e mi dà la possibilità di eliminarle solo se non è già stato proiettato
@client.route('/allbook')
@login_required
def allbook():
    if current_user.gestore == 0 :
        id = current_user.get_id()
        proiezioni = []
        conn = engine.connect()
        trans = conn.begin()

        try:
            query_acquisti = "SELECT s.nome, f.titolo, p.data, p.ora, a.posti,a.id, CASE WHEN p.data > DATE(NOW()) or (p.data = DATE(NOW())   and p.ora >= CURRENT_TIME(1) )  THEN 0 ELSE 1 END AS delectable  FROM acquisti a JOIN proiezioni p ON(a.proiezione =  p.idproiezione) JOIN sale s ON(p.sala = s.nsala) JOIN film f ON(p.film = f.codfilm) WHERE a.utente = "+str(id)+" ORDER BY a.id DESC"
            result = conn.execute(query_acquisti)
            for n in result:
                local = [n[0],n[1],n[2], n[3] ,n[4],n[5],n[6]]
                proiezioni.append(local)
            trans.commit()
        except Exception as e:
            print(e)
            trans.rollback()
            print("rollback allbook")
        finally:
            conn.close()
            return render_template('allbook.html',proiezioni = proiezioni)
    else:
        return redirect(url_for('main.index'))
