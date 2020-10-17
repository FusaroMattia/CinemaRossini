import sqlalchemy
from sqlalchemy import create_engine, MetaData , Column,Table,Integer,String,Boolean,DATE,ForeignKey,TEXT
from sqlalchemy_utils import create_database, drop_database

engine = create_engine('sqlite:////mnt/c/Users/Angry442/Desktop/Python/ProgettoBasi/rossini.db', echo = True)
drop_database(engine.url)
create_database(engine.url)
metadata = MetaData()

#user = Table('user', metadata,Column('id',Integer, primary_key = True),Column('name',String , nullable = True ),Column('email',String , nullable = False ),Column('password',String , nullable = False ))

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




film = Table('film', metadata,Column('CodFilm',Integer, primary_key = True),
                                Column('titolo',Integer, nullable = False ),
                                Column('autore',Integer , ForeignKey('cast.IdCast'), nullable = False ),
                                Column('durata',Integer, nullable = False ),
                                Column('generi',Integer , ForeignKey('generi.IdGeneri'), nullable = True),
                                Column('lingua_originale',Boolean, nullable = True )
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

cast = Table('cast', metadata,Column('IdCast',Integer, primary_key = True),
                                Column('nome',String , nullable = True),
                                Column('cognome',String , nullable = False),
                                Column('genere',Integer , ForeignKey('generi.IdGeneri'), nullable = False),
                                Column('stato',String, nullable = True),
                                Column('data_nascita',DATE , nullable = False),
                                Column('descr',TEXT , nullable = False),
            )
sale = Table('sale', metadata,Column('NSala',Integer, primary_key = True),
                                Column('posti_totali',Integer, nullable = False ),
                                Column('posti_disabili',Integer, nullable = False ),
                                Column('prezzo_posti',Integer, nullable = False )
            )
proiezioni = Table('proiezioni', metadata,Column('idProiezione',Integer, primary_key = True),
                                Column('sala',Integer ,  ForeignKey('sale.NSala'), nullable = False),
                                Column('film',Integer ,   ForeignKey('film.CodFilm'), nullable = False),
                                Column('data',DATE, nullable = False ),
                                Column('ora',DATE, nullable = False ),
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


#UTENTI
conn.execute('INSERT INTO utenti("id","email","password","name","cognome","citta","stato","data_nascita","sesso","riduzione","gestore") VALUES("1","mattiafusaro8@gmail.com","sha256$REOk6wJn$e46761b392ec91074c032623a3fb02ab89bfd3d1b3cf9ad6b575d9d7582e8d37","Mattia","Fusaro","Venezia","Veneto","1999-09-09","M","10","1")  ')
conn.execute('INSERT INTO utenti("id","email","password","name","cognome","citta","stato","data_nascita","sesso","riduzione","gestore") VALUES("2","visi@gmail.com","sha256$REOk6wJn$e46761b392ec91074c032623a3fb02ab89bfd3d1b3cf9ad6b575d9d7582e8d37","Giacomo","Visinoni","Venezia","Veneto","1999-09-09","M","15","1")  ')
conn.execute('INSERT INTO utenti("id","email","password","name","cognome","citta","stato","data_nascita","sesso","riduzione","gestore") VALUES("3","oliva@gmail.com","sha256$REOk6wJn$e46761b392ec91074c032623a3fb02ab89bfd3d1b3cf9ad6b575d9d7582e8d37","Lorenzo","Oliva","Venezia","Veneto","1999-09-09","M","0","0")  ')
conn.execute('INSERT INTO utenti("id","email","password","name","cognome","citta","stato","data_nascita","sesso","riduzione","gestore") VALUES("4","anthony@gmail.com","sha256$REOk6wJn$e46761b392ec91074c032623a3fb02ab89bfd3d1b3cf9ad6b575d9d7582e8d37","Anthony","Fusaro","Venezia","Veneto","1999-09-09","M","2","0")  ')

#SALE
conn.execute('INSERT INTO sale("NSala","posti_totali","posti_disabili","prezzo_posti") VALUES("1","100","7","9") ')
conn.execute('INSERT INTO sale("NSala","posti_totali","posti_disabili","prezzo_posti") VALUES("2","200","3","7") ')
conn.execute('INSERT INTO sale("NSala","posti_totali","posti_disabili","prezzo_posti") VALUES("3","50","1","12") ')
conn.execute('INSERT INTO sale("NSala","posti_totali","posti_disabili","prezzo_posti") VALUES("4","125","5","8") ')

#PROIEZIONI
conn.execute('INSERT INTO proiezioni("idProiezione","sala","film","data","ora","posti_liberi","posti_occupati") VALUES("1","1","1","2020-10-15","20:00:00","97","3") ')
conn.execute('INSERT INTO proiezioni("idProiezione","sala","film","data","ora","posti_liberi","posti_occupati") VALUES("2","3","1","2020-10-15","22:00:00","50","0") ')
conn.execute('INSERT INTO proiezioni("idProiezione","sala","film","data","ora","posti_liberi","posti_occupati") VALUES("3","2","1","2020-10-15","18:00:00","200","0") ')
conn.execute('INSERT INTO proiezioni("idProiezione","sala","film","data","ora","posti_liberi","posti_occupati") VALUES("4","1","1","2020-10-15","16:00:00","100","0") ')


#ACQUISTI
conn.execute('INSERT INTO acquisti("id","utente","proiezione","posti") VALUES("1","1","1","12") ')
conn.execute('INSERT INTO acquisti("id","utente","proiezione","posti") VALUES("2","2","1","15") ')
conn.execute('INSERT INTO acquisti("id","utente","proiezione","posti") VALUES("3","3","1","18") ')


#GENERE
conn.execute('INSERT INTO genere("IdGenere","titolo","descr") VALUES("1","Azione","Film epico con sparatorie ed uccisioni") ')
conn.execute('INSERT INTO genere("IdGenere","titolo","descr") VALUES("2","Romantico","MlMl") ')


#GENERI
conn.execute('INSERT INTO generi("IdGeneri","genere1","genere2","genere3") VALUES("1","1","2",NULL) ')
conn.execute('INSERT INTO generi("IdGeneri","genere1","genere2","genere3") VALUES("2","1",NULL,NULL) ')


#CAST
conn.execute('INSERT INTO cast("IdCast","nome","cognome","genere","stato","data_nascita","descr") VALUES("1","Bruce","Wayne","2","USA","10/10/1914","Non ci serve è una macchina da guerra") ')


#FILM
conn.execute('INSERT INTO film("CodFilm","titolo","autore","durata","generi","lingua_originale") VALUES("1","Io sono leggenda","1","145","1","1") ')



conn.close()
