import sqlalchemy
from sqlalchemy import create_engine, MetaData , Column,Table,Integer,String,Boolean,DATE,ForeignKey,TEXT,TIME
from sqlalchemy_utils import create_database, drop_database,database_exists

engine = create_engine("postgresql+psycopg2://admin:admin@localhost/rossini")

if not database_exists(engine.url):
    create_database(engine.url)

drop_database(engine.url)
create_database(engine.url)
metadata = MetaData()




ruolo = Table('ruolo', metadata,Column('id',Integer, primary_key = True),
                                Column('name',String , nullable = False, unique=True )
            )


utenti = Table('utenti', metadata,Column('id',Integer, primary_key = True),
                                Column('email',String , nullable = False , unique=True),
                                Column('password',String , nullable = False ),
                                Column('name',String , nullable = False ),
                                Column('cognome',String , nullable = False ),
                                Column('citta',String , nullable = True ),
                                Column('stato',String , nullable = True ),
                                Column('data_nascita',DATE , nullable = False ),
                                Column('sesso',String, nullable = False ) ,
                                Column('riduzione',Integer , nullable = False ) ,
                                Column('gestore',Integer , nullable = False ) ,
                                Column('roles',Integer, ForeignKey('ruoli.id') , nullable = True)
            )

ruoli = Table('ruoli', metadata,Column('id',Integer, primary_key = True),
                                Column('user_id',Integer , ForeignKey('utenti.id') , nullable = False ),
                                Column('role_id',Integer , ForeignKey('ruolo.id') ,nullable = False )
            )



genere = Table('genere', metadata,Column('idgenere',Integer, primary_key = True),
                                Column('titolo',String , nullable = False),
                                Column('descr',TEXT , nullable = False),
            )

generi = Table('generi', metadata,Column('idgeneri',Integer, primary_key = True),
                                Column('genere1',Integer, ForeignKey('genere.idgenere'), nullable = False),
                                Column('genere2',Integer, ForeignKey('genere.idgenere'), nullable = True),
                                Column('genere3',Integer, ForeignKey('genere.idgenere'), nullable = True),

        )

attori = Table('attori', metadata,Column('idattori',Integer, primary_key = True),
                                Column('nome',String , nullable = True),
                                Column('cognome',String , nullable = False),
                                Column('genere',Integer , ForeignKey('genere.idgenere'), nullable = False),
                                Column('stato',String, nullable = True),
                                Column('data_nascita',DATE , nullable = False),
                                Column('descr',TEXT , nullable = False),
            )
film = Table('film', metadata,Column('codfilm',Integer, primary_key = True),
                                Column('titolo',String, nullable = False ),
                                Column('autore',Integer , ForeignKey('attori.idattori'), nullable = False ),
                                Column('durata',Integer, nullable = False ),
                                Column('generi',Integer , ForeignKey('generi.idgeneri'), nullable = True),
                                Column('lingua_originale',Boolean, nullable = True )
            )

sale = Table('sale', metadata,Column('nsala',Integer, primary_key = True),
                                Column('nome',String , nullable = True),
                                Column('posti_totali',Integer, nullable = False ),
                                Column('posti_disabili',Integer, nullable = False ),
                                Column('prezzo_posti',Integer, nullable = False )
            )
proiezioni = Table('proiezioni', metadata,Column('idproiezione',Integer, primary_key = True),
                                Column('sala',Integer ,  ForeignKey('sale.nsala'), nullable = False),
                                Column('film',Integer ,   ForeignKey('film.codfilm'), nullable = False),
                                Column('data',DATE, nullable = False ),
                                Column('ora',TIME, nullable = False ),
                                Column('posti_liberi',Integer, nullable = False ),
                                Column('posti_occupati',Integer, nullable = False )
            )

acquisti = Table('acquisti', metadata,Column('id',Integer, primary_key = True),
                                Column('utente',Integer ,  ForeignKey('utenti.id'), nullable = False ),
                                Column('proiezione',Integer , ForeignKey('proiezioni.idproiezione'), nullable = False   ),
                                Column('posti',Integer , nullable = False )
            )
metadata.create_all(engine)

conn = engine.connect()

conn.execute("ALTER TABLE acquisti ADD CONSTRAINT posto_unico UNIQUE (proiezione, posti);")


#RUOLO
conn.execute("INSERT INTO ruolo(name) VALUES('Admin') ")
conn.execute("INSERT INTO ruolo(name) VALUES('Gestore') ")
conn.execute("INSERT INTO ruolo(name) VALUES('Cliente') ")



#UTENTI
conn.execute("INSERT INTO utenti(id,email,password,name,cognome,citta,stato,data_nascita,sesso,riduzione,gestore) VALUES('98','mattiafusaro8@gmail.com','1234','Mattia','Fusaro','Venezia','Veneto','1999-09-09','male','0','1')  ")
conn.execute("INSERT INTO utenti(id,email,password,name,cognome,citta,stato,data_nascita,sesso,riduzione,gestore) VALUES('99','mattia@gmail.com','1234','Tia','Fusaro','Venezia','Veneto','1999-09-09','male','0','0')  ")


#ruoli
#conn.execute("INSERT INTO ruoli(id,user_id,role_id) VALUES('0','98','1') ")
#conn.execute("INSERT INTO ruoli(id,user_id,role_id) VALUES('1','99','2') ")

#conn.execute("UPDATE utenti SET roles = 0 WHERE id = 0")
#conn.execute("UPDATE utenti SET roles = 1 WHERE id = 1")

#SALE
conn.execute("INSERT INTO sale(nome,posti_totali,posti_disabili,prezzo_posti) VALUES('Dedalo','100','7','9') ")
conn.execute("INSERT INTO sale(nome,posti_totali,posti_disabili,prezzo_posti) VALUES('Icaro','200','3','7') ")
conn.execute("INSERT INTO sale(nome,posti_totali,posti_disabili,prezzo_posti) VALUES('Ulisse','50','1','12') ")
conn.execute("INSERT INTO sale(nome,posti_totali,posti_disabili,prezzo_posti) VALUES('Percy','150','5','8') " )

#GENERE
conn.execute("INSERT INTO genere(titolo,descr) VALUES('Animazione',' ')" )
conn.execute("INSERT INTO genere(titolo,descr) VALUES('Avventura',' ')" )
conn.execute("INSERT INTO genere(titolo,descr) VALUES('Biografico',' ')" )
conn.execute("INSERT INTO genere(titolo,descr) VALUES('Commedia',' ')" )
conn.execute("INSERT INTO genere(titolo,descr) VALUES('Documentario',' ')" )
conn.execute("INSERT INTO genere(titolo,descr) VALUES('Pornografico',' ')" )
conn.execute("INSERT INTO genere(titolo,descr) VALUES('Erotico',' ')" )
conn.execute("INSERT INTO genere(titolo,descr) VALUES('Fantascienza',' ')" )
conn.execute("INSERT INTO genere(titolo,descr) VALUES('Fanstasy',' ')" )
conn.execute("INSERT INTO genere(titolo,descr) VALUES('Guerra',' ')" )
conn.execute("INSERT INTO genere(titolo,descr) VALUES('Horror',' ')" )
conn.execute("INSERT INTO genere(titolo,descr) VALUES('Musical',' ')" )
conn.execute("INSERT INTO genere(titolo,descr) VALUES('Storico',' ')" )
conn.execute("INSERT INTO genere(titolo,descr) VALUES('Thriller',' ')" )
conn.execute("INSERT INTO genere(titolo,descr) VALUES('Western',' ')" )



#GENERI
conn.execute("INSERT INTO generi(genere1,genere2,genere3) VALUES('1','2',NULL) ")
conn.execute("INSERT INTO generi(genere1,genere2,genere3) VALUES('1',NULL,NULL) ")


#CAST

conn.execute("INSERT INTO attori(nome,cognome,genere,stato,data_nascita,descr) VALUES('Bruce','Schetta','1','California','1914-10-10','Se el mejo tocco de oro') ")

#FILM
conn.execute("INSERT INTO film(titolo,autore,durata,generi,lingua_originale) VALUES('Io sono leggenda','1','145','1','1')" )
conn.execute("INSERT INTO film(titolo,autore,durata,generi,lingua_originale) VALUES('Transformers','1','200','1','1') ")
conn.execute("INSERT INTO film(titolo,autore,durata,generi,lingua_originale) VALUES('Alba','1','245','1','1') ")

#PROIEZIONI
conn.execute("INSERT INTO proiezioni(sala,film,data,ora,posti_liberi,posti_occupati) VALUES('1','1','2020-10-15','20:00:00','100','0') ")
conn.execute("INSERT INTO proiezioni(sala,film,data,ora,posti_liberi,posti_occupati) VALUES('2','2','2020-10-15','22:00:00','200','0') ")
conn.execute("INSERT INTO proiezioni(sala,film,data,ora,posti_liberi,posti_occupati) VALUES('3','3','2020-10-15','18:00:00','50','0') ")
conn.execute("INSERT INTO proiezioni(sala,film,data,ora,posti_liberi,posti_occupati) VALUES('4','3','2020-10-15','16:00:00','120','0') ")


#ACQUISTI
#conn.execute('INSERT INTO acquisti("id","utente","proiezione","posti") VALUES("1","1","1","12") ')
#conn.execute('INSERT INTO acquisti("id","utente","proiezione","posti") VALUES("2","2","1","15") ')
#conn.execute('INSERT INTO acquisti("id","utente","proiezione","posti") VALUES("3","3","1","18") ')



#RUOLI
role_gestore = "SELECT 1 FROM pg_roles WHERE rolname='gestore'"
role_cliente = "SELECT 1 FROM pg_roles WHERE rolname='cliente'"


if role_gestore:
    conn.execute("DROP ROLE gestore ")
    conn.execute("CREATE ROLE gestore WITH LOGIN PASSWORD 'ciao' ")
else:
    conn.execute("CREATE ROLE gestore WITH LOGIN PASSWORD 'ciao' ")

if role_cliente:
    conn.execute("DROP ROLE cliente ")
    conn.execute("CREATE ROLE cliente WITH LOGIN PASSWORD 'ciao' ")
else:
    conn.execute("CREATE ROLE cliente WITH LOGIN PASSWORD 'ciao' ")




#conn.execute("DROP ROLE admin")
#conn.execute("CREATE ROLE admin WITH PASSWORD '1234'")


#PERMESSI
#SELECT
conn.execute("GRANT CONNECT ON DATABASE rossini TO gestore")
conn.execute("GRANT CONNECT ON DATABASE rossini TO cliente")

conn.execute("GRANT USAGE ON SCHEMA public TO gestore")
conn.execute("GRANT USAGE ON SCHEMA public TO cliente")

conn.execute("GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO gestore")
conn.execute("GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO gestore")


conn.execute("GRANT SELECT ON film TO PUBLIC; GRANT SELECT ON proiezioni TO PUBLIC; GRANT SELECT ON sale TO PUBLIC; GRANT SELECT ON acquisti TO gestore; GRANT SELECT ON utenti TO PUBLIC; GRANT SELECT ON attori TO PUBLIC; GRANT SELECT ON generi TO PUBLIC; GRANT SELECT ON genere TO PUBLIC;")

#INSERT
conn.execute("GRANT INSERT ON genere TO gestore; GRANT INSERT ON generi TO gestore; GRANT INSERT ON attori TO gestore; GRANT INSERT ON film TO gestore; GRANT INSERT ON sale TO gestore; GRANT INSERT ON proiezioni TO gestore;")
conn.execute("GRANT INSERT ON acquisti TO cliente; ")

#UPDATE
conn.execute("GRANT UPDATE ON genere TO gestore; GRANT UPDATE ON generi TO gestore; GRANT UPDATE ON attori TO gestore; GRANT UPDATE ON film TO gestore; GRANT UPDATE ON sale TO gestore; GRANT UPDATE ON proiezioni TO gestore; GRANT UPDATE ON acquisti TO gestore; GRANT UPDATE ON utenti TO gestore;")
conn.execute("GRANT UPDATE ON proiezioni TO cliente;")
#DELETE
conn.execute("GRANT DELETE ON genere TO gestore; GRANT DELETE ON generi TO gestore; GRANT DELETE ON utenti TO gestore; GRANT DELETE ON attori TO gestore; GRANT DELETE ON film TO gestore; GRANT DELETE ON sale TO gestore; GRANT DELETE ON proiezioni TO gestore; GRANT DELETE ON acquisti TO gestore;")
conn.execute("GRANT DELETE ON acquisti TO cliente;")







conn.close()
