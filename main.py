from flask import Blueprint, render_template, redirect, url_for, request,flash,session
from flask_login import LoginManager, login_user, logout_user, current_user, AnonymousUserMixin
from . import db
from sqlalchemy import create_engine, text
from flask_user import login_required,UserManager, UserMixin, SQLAlchemyAdapter,roles_required

main = Blueprint('main', __name__)
engine = create_engine("postgresql+psycopg2://cliente:ciao@localhost/rossini")


@main.route('/')
def index():
    conn = engine.connect()

    query = "SELECT * FROM proiezioni  ORDER BY data  DESC, ora ASC"
    results = conn.execute(query)

    proiezioni = []

    for n in results:
        proiezioni_nsala = n[1]
        proiezioni_codfilm = n[2]


        query = "SELECT titolo FROM film WHERE codfilm = "+str(proiezioni_codfilm)
        result = conn.execute(query)
        titolo = result.fetchone()
        proiezioni_titolo = titolo[0]

        query = "SELECT nome FROM sale WHERE nsala = "+str(proiezioni_nsala)
        result = conn.execute(query)
        sala = result.fetchone()
        proiezioni_nome_sala = sala[0]

        cell = [n[0],proiezioni_nsala,proiezioni_codfilm,proiezioni_titolo,proiezioni_nome_sala,n[3],n[4],n[5],n[6]]
        proiezioni.append(cell)


    titoli_distinti = []
    query = "SELECT codfilm,titolo FROM film "
    titoli= conn.execute(query)
    for x in titoli:
        local =   [   x[0], x[1]  ]
        titoli_distinti.append(local)
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
    if current_user.gestore == 0 and request.method == "POST" :
       film = request.form.get('film')
       conn = engine.connect()

       query = "SELECT * FROM film WHERE codfilm = "+str(film)
       results = conn.execute(query)
       record_film = results.fetchone()

       conn.close()
       return render_template('film.html', film = record_film,generi = "ciao")
    else:
       return redirect(url_for('main.index'))
