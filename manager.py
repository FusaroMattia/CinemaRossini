from flask import Blueprint, render_template, redirect, url_for, request,flash,session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, AnonymousUserMixin
from . import db
from sqlalchemy import create_engine, text
from flask_user import login_required,UserManager, UserMixin, SQLAlchemyAdapter,roles_required
import sqlite3

manager = Blueprint('manager', __name__)
engine = create_engine("postgresql+psycopg2://admin:admin@localhost/rossini")
connection = engine.raw_connection()
conn = engine.connect()
trans = conn.begin()

@manager.route('/addfilm',  methods=['POST'])
#@roles_required('Gestore')
def addfilm_post():
    if request.method == "POST" :
       titolo_film = request.form.get('titolo')
       autore_film = request.form.get('autore')
       durata_film = request.form.get('durata')
       genere_obbligatorio_film = request.form.get('genere1')
       tot_generi = 1
       genere_opzionale1_film = request.form.get('genere2')
       if genere_opzionale1_film  != 'empty' :
           tot_generi = tot_generi+1

       genere_opzionale2_film = request.form.get('genere3')
       if genere_opzionale2_film  != 'empty' :
           tot_generi = tot_generi + 1

       lingua_originale_film = request.form.get('lingua_originale')
       try:
           if tot_generi == 1:
               query = "INSERT INTO generi(genere1) VALUES('"+str(genere_obbligatorio_film)+"') RETURNING *"
           elif tot_generi == 1:
               query = "INSERT INTO generi(genere1,genere2) VALUES('"+str(genere_obbligatorio_film)+"','"+str(genere_opzionale1_film)+"') RETURNING *"
           else:
               query = "INSERT INTO generi(genere1,genere2,genere3) VALUES('"+str(genere_obbligatorio_film)+"','"+str(genere_opzionale1_film)+"','"+str(genere_opzionale2_film)+"') RETURNING *"
           result = conn.execute(query)
           new_id = result.fetchone()
           id_generi = new_id[0]
           query = "INSERT INTO film(titolo,autore,durata,generi,lingua_originale) VALUES('"+str(titolo_film)+"','"+str(autore_film)+"','"+str(durata_film)+"','"+str(id_generi)+"','"+str(lingua_originale_film)+"')"
           conn.execute(query)
           trans.commit()
       except:
              trans.rollback()
              print("rollback")

    return redirect(url_for("main.index"))

@manager.route('/addfilm')
#@roles_required('Gestore')
def addfilm():
    if current_user.is_authenticated :
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





        return render_template('addfilm.html',generi=generi_html,registi=registi_html)
    else:
        return redirect(url_for("main.profile"))

@manager.route('/addevent',  methods=['POST'] )
#@roles_required('Gestore')
def addevent_post():
    if request.method == "POST" :
       sala = request.form.get('sala')
       film = request.form.get('film')
       data = request.form.get('data')
       ora = request.form.get('ora')

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

    return redirect(url_for("main.index"))


@manager.route('/addevent')
#@roles_required('Gestore')
def addevent():
    if current_user.is_authenticated :
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





        return render_template('addevent.html',sale=sale_html,film=film_html)
    else:
        return redirect(url_for("main.profile"))

@manager.route('/statistic')
#@roles_required('Gestore')
def statistic():
    return 0
