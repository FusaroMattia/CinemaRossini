from flask import Blueprint, render_template, redirect, url_for, request,flash,session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, AnonymousUserMixin
from . import db
from sqlalchemy import create_engine, text
import sqlite3

main = Blueprint('main', __name__)
conn = sqlite3.connect('rossini.db', check_same_thread=False)
cursor = conn.cursor()

@main.route('/')
def index():
    query = "SELECT * FROM proiezioni  ORDER BY data  DESC, ora ASC"
    cursor.execute(query)
    results = cursor.fetchmany(12)
    array_films = []
    array_film = []
    for n in results:
        sala = n[1]
        film = n[2]
        query = "SELECT titolo FROM film WHERE CodFilm = "+str(film)
        cursor.execute(query)
        titolo = cursor.fetchone()
        array_film.append(titolo)

        query = "SELECT nome FROM sale WHERE NSala = "+str(sala)
        cursor.execute(query)
        nome_sala = cursor.fetchone()
        array_film.append(nome_sala)
        array_film.append(n[3])
        array_film.append(n[4])
        array_film.append(n[5])
        array_film.append(n[6])
        array_films.append(array_film)
        print(array_films)
        array_film.clear()




    return render_template('index.html', results = array_film)

@main.route('/profile')
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

       return render_template('film.html')
    else:
       return redirect(url_for('main.index'))
