# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, redirect, url_for, request,flash,session
from flask_login import LoginManager, login_user, logout_user, current_user, AnonymousUserMixin
from . import db
from sqlalchemy import create_engine, text
from flask_user import login_required,UserManager, UserMixin, SQLAlchemyAdapter,roles_required

# PAGINA .PY INZIALE, IN CUI HO LE PRINCIPALI ROUTE
# mi connetto attraverso il ruolo cliente, il quale può eseguire solo select

# lo riconosco come main dal mio __init__
main = Blueprint('main', __name__)

#creo l'engine attraverso il ruolo cliente
engine = create_engine("postgresql+psycopg2://cliente:ciao@localhost/rossini")


# Viene caricata ogni volta che accedo al sito, appunto è l'index in cui creo due variabili
# che popolerò così:
#           proiezioni --> conterrà tutte le info delle proiezioni della giornata corrente (prendendomi nome sala e titolo film dalle rispettive tabelle)
#           titoli_distinti --> conterrà tutti i titoli dei film presenti nel nostro database per la ricerca successiva
@main.route('/')
def index():
    proiezioni = []
    titoli_distinti = []
    conn = engine.connect()
    trans = conn.begin()
    try:
        query_proiezioni = "SELECT p.idproiezione, p.sala, p.film, s.nome, f.titolo, p.data, p.ora, p.posti_liberi, p.posti_occupati FROM proiezioni p  JOIN sale s ON(p.sala = s.nsala) JOIN film f ON(p.film = f.codfilm) WHERE p.data  = DATE(NOW()) ORDER BY data  DESC, ora ASC "
        risultati = conn.execute(query_proiezioni)

        for n in risultati:
            local = [n[0],n[1],n[2],n[3],n[4],n[5],n[6],n[7],n[8]]
            proiezioni.append(local)

        query_titoli = "SELECT codfilm,titolo FROM film "
        risultato = conn.execute(query_titoli)

        for x in risultato:
            local =   [   x[0], x[1]  ]
            titoli_distinti.append(local)
        trans.commit()
    except Exception as e:
        print(e)
        trans.rollback()
        print("rollback index")
    finally:
        conn.close()
        return render_template('index.html', results = proiezioni, tutti=titoli_distinti)

# Route che viene caricata ogni volta che ci logghiamo o vogliomo vedere le nostre info
# Necessita di essere autenticati
# Non fa altro che restituire i dati sensibili dell'utente
@main.route('/profile')
@login_required
def profile():
    if current_user.is_authenticated :
        id = current_user.get_id()
        conn = engine.connect()
        trans = conn.begin()
        try:
            query_utente = "SELECT * FROM utenti WHERE id = "+id
            risultato = conn.execute(query_utente)
            utente = risultato.fetchone()
            trans.commit()
        except:
            trans.rollback()
            print("rollback user")
        finally:
            conn.close()
            return render_template('profile.html', results=utente)
    else:
        return redirect(url_for('auth.login'))


# Route che viene caricata ogni volta che clicchiamo su un titolo nell'index.html o nella ricerca per titolo
# Necessita di avere una variabile passata con metodo "post"
# In base a ciò che passiamo restituirà le infomazioni del film (titolo. nome dei generi ecc..) salvate nella variabile film
# E tutte le proiezioni di oggi e prossime ad oggi
@main.route('/film' , methods=['POST'])
def film():
    if request.method == "POST" and request.form.get('film'):
       film = request.form.get('film')
       tabella = []
       conn = engine.connect()
       trans = conn.begin()
       try:
           #richiedo tutte le info del film da me scelto
           if film.isnumeric():
               query = "SELECT f.codfilm, f.titolo, a.nome, a.cognome, f.durata, g1.titolo, g2.titolo , g3.titolo ,f.lingua_originale,a.idattori FROM film f JOIN generi g ON(f.generi = g.idgeneri) JOIN genere g1 ON(g.genere1 = g1.idgenere) LEFT JOIN genere g2 ON(g.genere2 = g2.idgenere) LEFT JOIN genere g3 ON(g.genere3 = g3.idgenere) JOIN attori a ON (a.idattori = f.autore)  WHERE f.codfilm ="+str(film)
           else:
               query = "SELECT f.codfilm, f.titolo, a.nome, a.cognome, f.durata, g1.titolo, g2.titolo , g3.titolo ,f.lingua_originale,a.idattori  FROM film f JOIN generi g ON(f.generi = g.idgeneri) JOIN genere g1 ON(g.genere1 = g1.idgenere) LEFT JOIN genere g2 ON(g.genere2 = g2.idgenere) LEFT JOIN genere g3 ON(g.genere3 = g3.idgenere) JOIN attori a ON (a.idattori = f.autore)  WHERE f.titolo ='"+str(film)+"'"

           risultato = conn.execute(query)
           record_film = risultato.fetchone()
           film = [record_film[0],record_film[1],record_film[2],record_film[3],record_film[4],record_film[5],record_film[6],record_film[7],record_film[8],record_film[9]]

           #richiedo tutte le proiezioni da oggi in poi per il film scelto
           query_proiezioni = "SELECT p.idproiezione,s.nome, p.data, p.ora, p.posti_liberi, p.posti_occupati FROM proiezioni p JOIN sale s ON(p.sala = s.nsala) WHERE p.data  >= DATE(NOW()) AND p.film = " +str(film[0])+ " ORDER BY data  DESC, ora ASC"
           risultati = conn.execute(query_proiezioni)


           for n in risultati:
               local_proiezioni = [n[0], n[1] , n[2] , n[3] , n[4],n[5]]
               tabella.append(local_proiezioni)

           trans.commit()
       except Exception as e:
           print(e)
           trans.rollback()
           print("rollback film")
       finally:
           conn.close()
           return render_template('film.html', film = film, tabella = tabella)
    else:
       return redirect(url_for('main.index'))


# Route che viene caricata ogni volta che clicchiamo sul regista nell'film.html
# Necessita di avere una variabile passata con metodo "post"
# In base a ciò che passiamo restituirà le infomazioni del regista  salvate nella variabile autore_html
@main.route('/author' , methods=['POST'])
def author():
    if request.method == "POST" and request.form.get('autore'):
        id_autore = request.form.get('autore')
        autore_html = []
        conn = engine.connect()
        trans = conn.begin()
        try:
            query_attori = " SELECT a.nome, a.cognome, g.titolo, a.stato, a.data_nascita, a.descr FROM attori a JOIN genere g ON (a.genere = g.idgenere) WHERE a.idattori = "+str(id_autore)
            risultato = conn.execute(query_attori)
            record_autore = risultato.fetchone()
            autore_html = [  record_autore[0],record_autore[1],record_autore[2],record_autore[3],record_autore[4],record_autore[5] ]

            trans.commit()
        except Exception as e:
            print(e)
            trans.rollback()
            print("rollback author")

        finally:
            conn.close()
            return render_template('author.html', results=autore_html)

    else:
        return redirect(url_for('main.index'))
