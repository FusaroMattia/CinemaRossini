# -*- coding: UTF-8 -*-
from flask import Blueprint, render_template, redirect, url_for, request,flash,session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, AnonymousUserMixin
from . import db
from sqlalchemy import create_engine, text
from flask_user import login_required,UserManager, UserMixin, SQLAlchemyAdapter,roles_required
import sqlite3


# PAGINA .PY DEDICATA AL RUOLO gestore, IN CUI HO LE ROUTE ESEGUIBILI
# mi connetto attraverso il ruolo gestore

manager = Blueprint('manager', __name__)
engine = create_engine("postgresql+psycopg2://gestore:ciao@localhost/rossini")

# Route che viene caricata ogni volta che clicchiamo sul tasto AGGIUNGI FILM nel addfilm.html
# Necessita di avere una variabile passata con metodo "post" e che io sia un gestore
# Essa crerà prima la sequenza di generi del mio film e solo se posso aggiungerla allora cercherà di aggiungere un film al database
# ricordiamo che il titolo del film è unico e se una delle due insert va in errore non viene aggiunto nessuno dei due
@manager.route('/addfilm',  methods=['POST'])
def addfilm_post():
    if current_user.gestore == 1 and request.method == "POST" :
       titolo_film = request.form.get('titolo')
       autore_film = request.form.get('autore')
       durata_film = request.form.get('durata')
       genere_obbligatorio_film = request.form.get('genere1')
       genere_opzionale1_film = request.form.get('genere2')
       genere_opzionale2_film = request.form.get('genere3')
       lingua_originale_film = request.form.get('lingua_originale')
       if not lingua_originale_film:
           lingua_originale_film = False

       conn = engine.connect()
       trans = conn.begin()
       try:#il film ha un genere obbligatorio principale e 2 opzionali o sotto generi
           if not genere_opzionale1_film and not genere_opzionale2_film:
               query = "INSERT INTO generi(genere1) VALUES('"+str(genere_obbligatorio_film)+"') RETURNING *"
           elif not genere_opzionale2_film:
               query = "INSERT INTO generi(genere1,genere2) VALUES('"+str(genere_obbligatorio_film)+"','"+str(genere_opzionale1_film)+"') RETURNING *"
           else:
               query = "INSERT INTO generi(genere1,genere2,genere3) VALUES('"+str(genere_obbligatorio_film)+"','"+str(genere_opzionale1_film)+"','"+str(genere_opzionale2_film)+"') RETURNING *"

           result = conn.execute(query)
           new_id = result.fetchone()
           id_generi = new_id[0]
           #solo se ho creato la sequenza di generi allora aggiungo il film (IL RETURNING restituisce l'id del record dei generi appena aggiunto)
           query = "INSERT INTO film(titolo,autore,durata,generi,lingua_originale) VALUES('"+str(titolo_film)+"','"+str(autore_film)+"','"+str(durata_film)+"','"+str(id_generi)+"','"+str(lingua_originale_film)+"')"
           conn.execute(query)
           trans.commit()
       except Exception as e:
           print(e)
           trans.rollback()
           print("rollback addfilm")
       finally:
           conn.close()
           return redirect(url_for("main.index"))


# Route che viene caricata ogni volta che clicchiamo sul tasto FILM nel profile.html
# Necessita che io sia un gestore e io sia autenticato
# Essa restituirà tutti i generi ed autori presenti nel mio db
# Per dare la possibilità di rifersi a quelli già presenti senza crearne sempre di nuovi
@manager.route('/addfilm')
def addfilm():
    if current_user.is_authenticated and current_user.gestore == 1 :
        conn = engine.connect()
        trans = conn.begin()
        try:
            query = "SELECT idgenere,titolo FROM genere  ORDER BY idgenere  ASC"
            generi = conn.execute(query)
            generi_html = []
            for row in generi:
                local_generi = [ [row[0],row[1]] ]
                generi_html.extend(local_generi)
            query = "SELECT idattori,cognome FROM attori  ORDER BY idattori  ASC"
            registi = conn.execute(query)
            registi_html = []
            for row in registi:
                local_registi = [ [row[0],row[1]] ]
                registi_html.extend(local_registi)

            trans.commit()
        except Exception as e:
            print(e)
            trans.rollback()
            print("rollback addfilm")
        finally:
            conn.close()
            return render_template('addfilm.html',generi=generi_html,registi=registi_html)
    else:
        return redirect(url_for("main.profile"))

# Route che viene caricata ogni volta che clicchiamo sul tasto AUTORI nel profile.html
# Necessita che io sia un gestore e io sia autenticato
# Essa restituirà tutti i generi presenti nel mio db
# Per dare la possibilità di rifersi a quelli già presenti senza crearne sempre di nuovi
@manager.route('/addauthor', )
def addauthor():
    if current_user.is_authenticated and current_user.gestore == 1  :
        conn = engine.connect()
        query = "SELECT idgenere,titolo FROM genere  ORDER BY idgenere  ASC"
        generi = conn.execute(query)
        generi_html = []
        for row in generi:
            local_generi = [ [row[0],row[1]] ]
            generi_html.extend(local_generi)
        conn.close()
        return render_template('addauthor.html',generi = generi_html)
    else:
        return redirect(url_for("main.index"))


# Route che viene caricata ogni volta che clicchiamo sul tasto AGGIUNGI AUTORE nel addauthor.html
# Necessita di avere una variabile passata con metodo "post" e che io sia un gestore
# Essa cercherà di aggiungere un autore al mio database, in questo caso non ci sono restrizioni se non sul genere, che però può essere scelto solo attraverso una select
@manager.route('/addauthor',  methods=['POST'])
def addauthor_post():
    if current_user.gestore == 1 and request.method == "POST" :
        nome_autore = request.form.get('nome')
        cognome_autore = request.form.get('cognome')
        genere_autore = request.form.get('genere')
        stato_autore = request.form.get('stato')
        data_nascita_autore = request.form.get('data_nascita')
        descr_autore = request.form.get('descr')
        conn = engine.connect()
        trans = conn.begin()
        try:
            query_attori = "INSERT INTO attori(nome,cognome,genere,stato,data_nascita,descr) VALUES('"+str(nome_autore)+"','"+str(cognome_autore)+"','"+str(genere_autore)+"','"+str(stato_autore)+"','"+str(data_nascita_autore)+"','"+str(descr_autore)+"') "
            conn.execute(query_attori)
            trans.commit()
        except:
            trans.rollback()
            print("rollback addauthor")
        finally:
            conn.close()
            return redirect(url_for("main.index"))
    else:
        return redirect(url_for("main.index"))


# Route che viene caricata ogni volta che clicchiamo sul tasto AGGIUNGI PROIEZIONE nel addevent.html
# Necessita di avere una variabile passata con metodo "post" e che io sia un gestore
# Essa cercherà di aggiungere una proiezione al mio database, prima però devo prendermi i posti totali della sala scelta
@manager.route('/addevent',  methods=['POST'] )
def addevent_post():
    if current_user.gestore == 1 and request.method == "POST" :
       sala = request.form.get('sala')
       film = request.form.get('film')
       data = request.form.get('data')
       ora = request.form.get('ora')

       conn = engine.connect()
       trans = conn.begin()
       try:
           query = "SELECT * FROM sale  WHERE nsala ="+str(sala)
           result = conn.execute(query)
           sale_row = result.fetchone()
           n_posti = sale_row[2]
           query = "INSERT INTO proiezioni(sala,film,data,ora,posti_liberi,posti_occupati) VALUES('"+str(sala)+"','"+str(film)+"','"+str(data)+"','"+str(ora)+"','"+str(n_posti)+"','0')"
           conn.execute(query)
           trans.commit()
       except:
              trans.rollback()
              print("rollback")
       conn.close()
    return redirect(url_for("main.index"))

# Route che viene caricata ogni volta che clicchiamo sul tasto PROIEZIONE nel profile.html
# Necessita che io sia un gestore e io sia autenticato
# Essa restituirà tutti i film e le sale presenti nel mio db
# Per dare la possibilità di rifersi a quelli già presenti senza crearne sempre di nuovi
@manager.route('/addevent')
def addevent():
    if current_user.is_authenticated and current_user.gestore == 1:
        conn = engine.connect()
        trans = conn.begin()
        query = "SELECT nsala,nome FROM sale  ORDER BY nsala  ASC"
        sale = conn.execute(query)
        sale_html = []
        for row in sale:
            local_sale = [ [row[0],row[1]] ]
            sale_html.extend(local_sale)

        query = "SELECT codfilm,titolo FROM film  ORDER BY codfilm  ASC"
        film = conn.execute(query)
        film_html = []
        for row in film:
            local_film = [ [row[0],row[1]] ]
            film_html.extend(local_film)
        conn.close()
        return render_template('addevent.html',sale=sale_html,film=film_html)
    else:
        return redirect(url_for("main.profile"))


# Route che viene caricata ogni volta che clicchiamo sul tasto STATISTICHE nel profile.html
# Necessita che io sia un gestore e io sia autenticato
# Essa restituirà
#
#
#
@manager.route('/statistic')
def statistic():
    if current_user.is_authenticated and current_user.gestore == 1:

        conn = engine.connect()
        trans = conn.begin()
        try:
            query_refresh_mv = "REFRESH MATERIALIZED VIEW prezzi_sala_mat"
            conn.execute(query_refresh_mv)
            query_incassi_totali_film= "SELECT f.titolo, SUM(v.incasso) AS incasso FROM prezzi_sala_mat v JOIN film f ON (v.film = f.codfilm) GROUP BY v.film, f.titolo"
            film = conn.execute(query_incassi_totali_film)
            film_html = []
            for row in film:
                local_film = [ [row[0], row[1]] ]
                film_html.extend(local_film)

            query_refresh_mv = "REFRESH MATERIALIZED VIEW prezzi_generi_mat"
            conn.execute(query_refresh_mv)

            query_incassi_totali_film= "SELECT v.genere, SUM(v.incasso) AS incasso FROM prezzi_generi_mat v GROUP BY v.genere"
            generi = conn.execute(query_incassi_totali_film)
            generi_html = []
            for row in generi:
                local_generi = [[row[0], row[1]] ]
                generi_html.extend(local_generi)

            query_refresh_mv = "REFRESH MATERIALIZED VIEW acquisti_utenti"
            conn.execute(query_refresh_mv)

            query_male_female= "SELECT u.sesso , SUM(a.acquisti) AS totali FROM acquisti_utenti a JOIN utenti u ON(a.utente = u.id) GROUP BY u.sesso"
            sex = conn.execute(query_male_female)
            sex_html = []
            tot = 0;
            for row in sex:
                n_row = int(row[1])

                tot = tot + n_row
                local_sex = [row[0], n_row]
                sex_html.append(local_sex)

            for x in sex_html:
                x[1] = (100 * row[1])/tot


            trans.commit()
        except Exception as e:
            print(e)
            trans.rollback()
            print("rollback")

        conn.close()
        return render_template('statistic.html',tot = film_html, generi = generi_html, sex = sex_html)


    return 0
