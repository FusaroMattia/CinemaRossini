import sqlalchemy
from sqlalchemy import create_engine, MetaData , Column,Table,Integer,String,Boolean,DATE,ForeignKey,TEXT
from sqlalchemy_utils import create_database, drop_database

engine = create_engine('sqlite:///:memory', echo = True)
drop_database(engine.url)
create_database(engine.url)
metadata = MetaData()

login = Table('login', metadata,Column('cod',Integer, primary_key = True),
                                Column('username',String , nullable = True ),
                                Column('email',String , nullable = False ),
                                Column('pwd',String , nullable = False )
            )

utenti = Table('utenti', metadata,Column('id',Integer, primary_key = True),
                                Column('nome',String , nullable = True ),
                                Column('cognome',String , nullable = False ),
                                Column('citta',String , nullable = True ),
                                Column('stato',String , nullable = True ),
                                Column('data_nascita',DATE , nullable = False ),
                                Column('sesso',String, nullable = False ) ,
                                Column('riduzione',Integer , nullable = False ) ,
                                Column('gestore',Boolean ) ,
                                Column('login',Integer , ForeignKey('login.cod'), nullable = False)
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
conn.execute('INSERT INTO utenti("id","nome","cognome","citta","stato","data_nascita","sesso","riduzione","gestore","pwd") VALUES("1","Mattia","Fusaro","Venezia","Veneto","09/12/1999","M","10","1","elangry442")  ')
conn.execute('INSERT INTO utenti("id","nome","cognome","citta","stato","data_nascita","sesso","riduzione","gestore","pwd") VALUES("2","Giacomo","Visinoni","Venezia","Veneto","30/04/1999","M","15","1","visi99")  ')
conn.execute('INSERT INTO utenti("id","nome","cognome","citta","stato","data_nascita","sesso","riduzione","gestore","pwd") VALUES("3","Lorenzo","Oliva","Venezia","Veneto","19/07/1999","M","0","0","oliva")  ')
conn.execute('INSERT INTO utenti("id","nome","cognome","citta","stato","data_nascita","sesso","riduzione","gestore","pwd") VALUES("4","Anthony","Fusaro","Venezia","Veneto","22/04/1996","M","2","0","fuxy")  ')

#SALE
conn.execute('INSERT INTO sale("NSala","posti_totali","posti_disabili","prezzo_posti") VALUES("1","100","7","9") ')
conn.execute('INSERT INTO sale("NSala","posti_totali","posti_disabili","prezzo_posti") VALUES("2","200","3","7") ')
conn.execute('INSERT INTO sale("NSala","posti_totali","posti_disabili","prezzo_posti") VALUES("3","50","1","12") ')
conn.execute('INSERT INTO sale("NSala","posti_totali","posti_disabili","prezzo_posti") VALUES("4","125","5","8") ')

#PROIEZIONI
conn.execute('INSERT INTO proiezioni("idProiezione","sala","film","data","ora","posti_liberi","posti_occupati") VALUES("1","1","1","15/10/2020","20:00:00","97","3") ')
conn.execute('INSERT INTO proiezioni("idProiezione","sala","film","data","ora","posti_liberi","posti_occupati") VALUES("2","3","1","15/10/2020","22:00:00","50","0") ')



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
