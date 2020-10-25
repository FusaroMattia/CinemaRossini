from flask import Blueprint, render_template, redirect, url_for, request,flash,session
from flask_login import LoginManager, login_user, logout_user, current_user, AnonymousUserMixin
from . import db
from sqlalchemy import create_engine, text
from flask_user import login_required,UserManager, UserMixin, SQLAlchemyAdapter,roles_required

main = Blueprint('main', __name__)
engine = create_engine("postgresql+psycopg2://cliente:ciao@localhost/rossini")


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

@main.route('/profile')
@login_required
def profile():
    if current_user.is_authenticated :
        id = current_user.get_id()
        conn = engine.connect()

        query = "SELECT * FROM utenti WHERE id = "+id
        results = conn.execute(query)
        utente = results.fetchone()
        conn.close()
        return render_template('profile.html', results=utente)
    else:
        return redirect(url_for('auth.login'))

@main.route('/film' , methods=['POST'])
#@roles_required('Cliente')
def film():
    if request.method == "POST" and request.form.get('film'):
       film = request.form.get('film')

       conn = engine.connect()
       trans = conn.begin()
       try:
           if film.isnumeric():
               query = "SELECT f.codfilm, f.titolo, a.nome, a.cognome, f.durata, g1.titolo, g2.titolo , g3.titolo ,f.lingua_originale FROM film f JOIN generi g ON(f.generi = g.idgeneri) JOIN genere g1 ON(g.genere1 = g1.idgenere) LEFT JOIN genere g2 ON(g.genere2 = g2.idgenere) LEFT JOIN genere g3 ON(g.genere3 = g3.idgenere) JOIN attori a ON (a.idattori = f.autore)  WHERE f.codfilm ="+str(film)
           else:
               query = "SELECT f.codfilm, f.titolo, a.nome, a.cognome, f.durata, g1.titolo, g2.titolo , g3.titolo ,f.lingua_originale FROM film f JOIN generi g ON(f.generi = g.idgeneri) JOIN genere g1 ON(g.genere1 = g1.idgenere) LEFT JOIN genere g2 ON(g.genere2 = g2.idgenere) LEFT JOIN genere g3 ON(g.genere3 = g3.idgenere) JOIN attori a ON (a.idattori = f.autore)  WHERE f.titolo ='"+str(film)+"'"
           risultato = conn.execute(query)
           record_film = risultato.fetchone()
           film = [record_film[0],record_film[1],record_film[2],record_film[3],record_film[4],record_film[5],record_film[6],record_film[7],record_film[8]]
           query_proiezioni = "SELECT p.idproiezione,s.nome, p.data, p.ora, p.posti_liberi, p.posti_occupati FROM proiezioni p JOIN sale s ON(p.sala = s.nsala) WHERE p.film = " +str(film[0])+ " ORDER BY data  DESC, ora ASC"
           risultati = conn.execute(query_proiezioni)
           tabella = []
           for n in risultati:
               local_proiezioni = [n[0], n[1] , n[2] , n[3] , n[4],n[5]]
               tabella.append(local_proiezioni)
           trans.commit()
       except:
           trans.rollback()
           print("rollback film")
       finally:
           conn.close()
           return render_template('film.html', film = film, tabella = tabella)
    else:
       return redirect(url_for('main.index'))
