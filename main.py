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

        cell = [n[0],proiezioni_nsala,proiezioni_codfilm,proiezioni_nome_sala,proiezioni_titolo,n[3],n[4],n[5],n[6]]
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
    if current_user.gestore == 0 and request.method == "POST" and request.form.get('film'):
       film = request.form.get('film')

       conn = engine.connect()
       if film.isnumeric():
           query = "SELECT * FROM film WHERE codfilm = "+str(film)
       else:
           query = "SELECT * FROM film WHERE titolo = '"+str(film)+"'"
       result = conn.execute(query)
       record_film = result.fetchone()

       #creo un array con tutti i nomi dei generi che asso poi all HTML
       generi_id = record_film[4]
       query = "SELECT * FROM generi WHERE idgeneri = "+str(generi_id)
       result = conn.execute(query)
       id_generi = result.fetchone()
       id_genere1 = id_generi[1]
       id_genere2 = id_generi[2]
       id_genere3 = id_generi[3]
       generi = [id_genere1, id_genere2, id_genere3]

       nomi_generi=[]
       for n in generi :
           if n :
               query= "SELECT titolo FROM genere WHERE idgenere = "+str(n)
               result = conn.execute(query)
               genere = result.fetchone()
               nome=genere[0]
               nomi_generi.append(nome)

       #Attori
       id_attore = record_film[2]
       query = "SELECT * FROM attori WHERE idattori = "+str(id_attore)
       result = conn.execute(query)
       query_attore = result.fetchone()
       nome_attore = query_attore[1]
       cognome_attore = query_attore[2]
       attore = [nome_attore, cognome_attore]

       #proiezioni
       id_film = record_film[0]
       query = "SELECT * FROM proiezioni WHERE film = " +str(id_film)+ "ORDER BY data  DESC, ora ASC"
       result = conn.execute(query)

       tabella = []
       for n in result:
           sala = n[1]
           query = "SELECT nome FROM sale WHERE nsala = "+str(sala)
           local = conn.execute(query)
           nome_sala = local.fetchone()
           local_proiezioni = [nome_sala[0], n[3] , n[4] , n[5] , n[6]]
           tabella.append(local_proiezioni)



       nome_film =  [id_film,record_film[1],id_attore,record_film[3],generi_id,record_film[5]]
       conn.close()
       return render_template('film.html', film = nome_film, generi = nomi_generi, attore = attore, tabella = tabella)
    else:
       return redirect(url_for('main.index'))
