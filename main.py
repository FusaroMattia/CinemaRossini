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
    query = "SELECT * FROM proiezioni  ORDER BY data  DESC, ora ASC"
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

       generi = nome_film[4]
       query = "SELECT * FROM generi WHERE idgeneri = "+str(generi)
       cursor.execute(query)
       nome_generi = cursor.fetchone()

       genere=generi[1]
       query= "SELECT * FROM genere WHERE idgenere = "+str(genere)


       return render_template('film.html', film = nome_film, generi = nome_generi)
    else:
       return redirect(url_for('main.index'))
