from flask import Blueprint, render_template, redirect, url_for, request,flash,session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, AnonymousUserMixin
from . import db
from sqlalchemy import create_engine, text
from flask_user import login_required,UserManager, UserMixin, SQLAlchemyAdapter,roles_required

main = Blueprint('main', __name__)
engine = create_engine("postgresql+psycopg2://admin:admin@localhost/rossini")
connection = engine.raw_connection()
cursor = connection.cursor()

@main.route('/')
def index():
    query = "SELECT * FROM proiezioni WHERE data = CURRENT_DATE ORDER BY data  DESC, ora ASC"
    cursor.execute(query)
    results = cursor.fetchmany(12)
    titoli = []
    sale = []
    for n in results:
        sala = n[1]
        film = n[2]

        query = "SELECT titolo FROM film WHERE codfilm = "+str(film)
        cursor.execute(query)
        titolo_film = cursor.fetchone()
        titoli.extend(titolo_film)

        query = "SELECT nome FROM sale WHERE sale.NSala = "+str(sala)
        cursor.execute(query)
        nome_sala = cursor.fetchone()
        sale.extend(nome_sala)

    return render_template('index.html', results = results, sale=sale,titoli=titoli)

@main.route('/profile')
@login_required
def profile():
    if current_user.is_authenticated :
        id = current_user.get_id()
        query = "SELECT * FROM utenti WHERE id = "+id
        cursor.execute(query)
        results = cursor.fetchone()
        return render_template('profile.html', results=results)
    else:
        return redirect(url_for('auth.login'))

@main.route('/film' , methods=['POST'])
def film():
    if request.method == "POST" :

       film = request.form.get('film')
       query = "SELECT * FROM film WHERE codfilm = "+str(film)
       cursor.execute(query)
       nome_film = cursor.fetchone()

       #creo un array con tutti i nomi dei generi che asso poi all HTML
       generi = nome_film[4]
       query = "SELECT * FROM generi WHERE idgeneri = "+str(generi)
       cursor.execute(query)
       id_generi = cursor.fetchone()
       id_genere1 = id_generi[1]
       id_genere2 = id_generi[2]
       id_genere3 = id_generi[3]
       generi = [id_genere1, id_genere2, id_genere3]
       nomi_generi=[]

       for n in generi :
           if n :
               query= "SELECT titolo FROM genere WHERE idgenere = "+str(n)
               cursor.execute(query)
               genere = cursor.fetchone()
               nome=genere[0]
               nomi_generi.append(nome)

       #Attori
       nome
       id_attore = nome_film[2]
       query = "SELECT * FROM attori WHERE idattori = "+str(id_attore)
       cursor.execute(query)
       query_attore = cursor.fetchone()
       nome_attore = query_attore[1]
       cognome_attore = query_attore[2]
       attore = [nome_attore, cognome_attore]

       #proiezioni
       query = "SELECT * FROM proiezioni WHERE film = " +str(nome_film[0])+" AND data = CURRENT_DATE ORDER BY data  DESC, ora ASC"
       cursor.execute(query)
       query_proiezione = cursor.fetchmany()




       return render_template('film.html', film = nome_film, generi = nomi_generi, attore = attore, tabella = query_proiezione)
    else:
       return redirect(url_for('main.index'))
