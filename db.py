import sqlalchemy
from sqlalchemy import create_engine, MetaData , Column,Table,Integer,String,Boolean,DATE,ForeignKey,TEXT,TIME
from sqlalchemy_utils import create_database, drop_database,database_exists

engine = create_engine("postgresql+psycopg2://admin:admin@localhost/rossini")

if not database_exists(engine.url):
    create_database(engine.url)

drop_database(engine.url)
create_database(engine.url)
metadata = MetaData()


ruoli = Table('ruoli', metadata,Column('id',Integer, primary_key = True),
                                Column('nome',String , nullable = False )
            )


utenti = Table('utenti', metadata,Column('id',Integer, primary_key = True),
                                Column('email',String , nullable = False ),
                                Column('password',String , nullable = False ),
                                Column('name',String , nullable = False ),
                                Column('cognome',String , nullable = False ),
                                Column('citta',String , nullable = True ),
                                Column('stato',String , nullable = True ),
                                Column('data_nascita',DATE , nullable = False ),
                                Column('sesso',String, nullable = False ) ,
                                Column('riduzione',Integer , nullable = False ) ,
                                Column('gestore',Integer )
            )





genere = Table('genere', metadata,Column('IdGenere',Integer, primary_key = True),
                                Column('titolo',String , nullable = False),
                                Column('descr',TEXT , nullable = False),
            )

generi = Table('generi', metadata,Column('IdGeneri',Integer, primary_key = True),
                                Column('genere1',Integer, ForeignKey('genere.IdGenere'), nullable = False),
                                Column('genere2',Integer, ForeignKey('genere.IdGenere'), nullable = True),
                                Column('genere3',Integer, ForeignKey('genere.IdGenere'), nullable = True),

        )

attori = Table('attori', metadata,Column('IdAttori',Integer, primary_key = True),
                                Column('nome',String , nullable = True),
                                Column('cognome',String , nullable = False),
                                Column('genere',Integer , ForeignKey('generi.IdGeneri'), nullable = False),
                                Column('stato',String, nullable = True),
                                Column('data_nascita',DATE , nullable = False),
                                Column('descr',TEXT , nullable = False),
            )
film = Table('film', metadata,Column('codfilm',Integer, primary_key = True),
                                Column('titolo',String, nullable = False ),
                                Column('autore',Integer , ForeignKey('attori.IdAttori'), nullable = False ),
                                Column('durata',Integer, nullable = False ),
                                Column('generi',Integer , ForeignKey('generi.IdGeneri'), nullable = True),
                                Column('lingua_originale',Boolean, nullable = True )
            )

sale = Table('sale', metadata,Column('nsala',Integer, primary_key = True),
                                Column('nome',String , nullable = True),
                                Column('posti_totali',Integer, nullable = False ),
                                Column('posti_disabili',Integer, nullable = False ),
                                Column('prezzo_posti',Integer, nullable = False )
            )
proiezioni = Table('proiezioni', metadata,Column('idProiezione',Integer, primary_key = True),
                                Column('sala',Integer ,  ForeignKey('sale.nsala'), nullable = False),
                                Column('film',Integer ,   ForeignKey('film.codfilm'), nullable = False),
                                Column('data',DATE, nullable = False ),
                                Column('ora',TIME, nullable = False ),
                                Column('posti_liberi',Integer, nullable = False ),
                                Column('posti_occupati',Integer, nullable = False )
            )

acquisti = Table('acquisti', metadata,Column('id',Integer, primary_key = True),
                                Column('utente',Integer ,  ForeignKey('utenti.id'), nullable = False ),
                                Column('proiezione',Integer , ForeignKey('proiezioni.idProiezione'), nullable = False   ),
                                Column('posti',Integer , nullable = False )
            )
metadata.create_all(engine)

conn = engine.connect()

#RUOLI
conn.execute("INSERT INTO ruoli(nome) VALUES('Admin') ")
conn.execute("INSERT INTO ruoli(nome) VALUES('Gestore') ")
conn.execute("INSERT INTO ruoli(nome) VALUES('Cliente') ")


#UTENTI
conn.execute("INSERT INTO utenti(email,password,name,cognome,citta,stato,data_nascita,sesso,riduzione,gestore) VALUES('mattiafusaro8@gmail.com','sha256$REOk6wJn$e46761b392ec91074c032623a3fb02ab89bfd3d1b3cf9ad6b575d9d7582e8d37','Mattia','Fusaro','Venezia','Veneto','1999-09-09','M','10','1')  ")

#SALE
conn.execute("INSERT INTO sale(nome,posti_totali,posti_disabili,prezzo_posti) VALUES('Dedalo','100','7','9') ")
conn.execute("INSERT INTO sale(nome,posti_totali,posti_disabili,prezzo_posti) VALUES('Icaro','200','3','7') ")
conn.execute("INSERT INTO sale(nome,posti_totali,posti_disabili,prezzo_posti) VALUES('Ulisse','50','1','12') ")
conn.execute("INSERT INTO sale(nome,posti_totali,posti_disabili,prezzo_posti) VALUES('Percy','125','5','8') " )

#GENERE
conn.execute("INSERT INTO genere(titolo,descr) VALUES('Azione','Film epico con sparatorie ed uccisioni')" )
conn.execute("INSERT INTO genere(titolo,descr) VALUES('Romantico','MlMl')" )


#GENERI
conn.execute("INSERT INTO generi(genere1,genere2,genere3) VALUES('1','2',NULL) ")
conn.execute("INSERT INTO generi(genere1,genere2,genere3) VALUES('1',NULL,NULL) ")


#CAST
#conn.execute("INSERT INTO cast( nome, cognome, genere, stato, data_nascita, descr) VALUES('Bruce','Wayne','2','USA','1914-10-10','Non ci serve è una macchina da guerra')")
conn.execute("INSERT INTO attori(nome,cognome,genere,stato,data_nascita,descr) VALUES('Bruce','Schetta','1','California','1914-10-10','Se el mejo tocco de oro') ")

#FILM
conn.execute("INSERT INTO film(titolo,autore,durata,generi,lingua_originale) VALUES('Io sono leggenda','1','145','1','1')" )
conn.execute("INSERT INTO film(titolo,autore,durata,generi,lingua_originale) VALUES('Transformers','1','200','1','1') ")

#PROIEZIONI
conn.execute("INSERT INTO proiezioni(sala,film,data,ora,posti_liberi,posti_occupati) VALUES('1','1','2020-10-15','20:00:00','97','3') ")
conn.execute("INSERT INTO proiezioni(sala,film,data,ora,posti_liberi,posti_occupati) VALUES('1','1','2020-10-15','22:00:00','100','0') ")
conn.execute("INSERT INTO proiezioni(sala,film,data,ora,posti_liberi,posti_occupati) VALUES('1','1','2020-10-15','18:00:00','100','0') ")
conn.execute("INSERT INTO proiezioni(sala,film,data,ora,posti_liberi,posti_occupati) VALUES('1','1','2020-10-15','16:00:00','100','0') ")


#ACQUISTI
#conn.execute('INSERT INTO acquisti("id","utente","proiezione","posti") VALUES("1","1","1","12") ')
#conn.execute('INSERT INTO acquisti("id","utente","proiezione","posti") VALUES("2","2","1","15") ')
#conn.execute('INSERT INTO acquisti("id","utente","proiezione","posti") VALUES("3","3","1","18") ')






conn.close()
