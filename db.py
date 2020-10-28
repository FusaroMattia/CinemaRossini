import sqlalchemy
from sqlalchemy import create_engine, MetaData , Column,Table,Integer,String,Boolean,DATE,ForeignKey,TEXT,TIME
from sqlalchemy_utils import create_database, drop_database,database_exists

#creo l'engine
engine = create_engine("postgresql+psycopg2://admin:admin@localhost/rossini")
engine_gestore = create_engine("postgresql+psycopg2://gestore:ciao@localhost/rossini")

#controllo se il database esiste, in caso contrario creo il mio database
if not database_exists(engine.url):
    create_database(engine.url)

drop_database(engine.url)
create_database(engine.url)
metadata = MetaData()



#creo le tabelle del mio database, creo prima le tabelle senza chavi esterne quindi senza riferimento ad altre tabelle gia esistenti cosicchè da evitare riferimenti ad elementi non ancora creati
#Tabella Utenti
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
                                Column('gestore',Integer , nullable = False )
            )

#Tabella Genere
genere = Table('genere', metadata,Column('idgenere',Integer, primary_key = True),
                                Column('titolo',String , nullable = False),
                                Column('descr',TEXT , nullable = False),
            )

#Tabella Sale
sale = Table('sale', metadata,Column('nsala',Integer, primary_key = True),
                                Column('nome',String , nullable = True),
                                Column('posti_totali',Integer, nullable = False ),
                                Column('posti_disabili',Integer, nullable = False ),
                                Column('prezzo_posti',Integer, nullable = False )
            )

#Tabella Generi
generi = Table('generi', metadata,Column('idgeneri',Integer, primary_key = True),
                                Column('genere1',Integer, ForeignKey('genere.idgenere'), nullable = False),
                                Column('genere2',Integer, ForeignKey('genere.idgenere'), nullable = True),
                                Column('genere3',Integer, ForeignKey('genere.idgenere'), nullable = True),

        )
#Tabella Attori
attori = Table('attori', metadata,Column('idattori',Integer, primary_key = True),
                                Column('nome',String , nullable = True),
                                Column('cognome',String , nullable = False),
                                Column('genere',Integer , ForeignKey('genere.idgenere'), nullable = False),
                                Column('stato',String, nullable = True),
                                Column('data_nascita',DATE , nullable = False),
                                Column('descr',TEXT , nullable = False),
            )

#Tabella Attori
film = Table('film', metadata,Column('codfilm',Integer, primary_key = True),
                                Column('titolo',String, nullable = False ),
                                Column('autore',Integer , ForeignKey('attori.idattori'), nullable = False ),
                                Column('durata',Integer, nullable = False ),
                                Column('generi',Integer , ForeignKey('generi.idgeneri'), nullable = True),
                                Column('lingua_originale',Boolean, nullable = True )
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

#creo i metadata e creo una connessione al mio engine cioè al mio database
metadata.create_all(engine)
conn = engine.connect()
#conn.execute("CREATE OR REPLACE FUNCTION REFRESH_PREZZI_SALA_MAT() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN REFRESH MATERIALIZED VIEW prezzi_sala_mat; RETURN NULL; END; $$;")
#conn.execute("CREATE TRIGGER REFRESH_PREZZI_SALA_MAT BEFORE INSERT OR UPDATE OR DELETE ON acquisti FOR EACH STATEMENT EXECUTE PROCEDURE REFRESH_PREZZI_SALA_MAT();")


conn.execute("ALTER TABLE acquisti ADD CONSTRAINT posto_unico UNIQUE (proiezione, posti);")
conn.execute("ALTER TABLE genere ADD CONSTRAINT genere_unico UNIQUE (titolo);")
conn.execute("ALTER TABLE film ADD CONSTRAINT film_unico UNIQUE (titolo);")




#UTENTI
#inserisco gli utenti all'interno della mia tabella utenti facendo un insert
conn.execute("INSERT INTO utenti(id,email,password,name,cognome,citta,stato,data_nascita,sesso,riduzione,gestore) VALUES('98','mattiafusaro8@gmail.com','1234','Mattia','Fusaro','Venezia','Veneto','1999-09-09','male','0','1')  ")
conn.execute("INSERT INTO utenti(id,email,password,name,cognome,citta,stato,data_nascita,sesso,riduzione,gestore) VALUES('99','mattia@gmail.com','1234','Tia','Fusaro','Venezia','Veneto','1999-09-09','male','0','0')  ")



#SALE
#creo le 4 sale del cinema con prezzi per posto differenti
conn.execute("INSERT INTO sale(nome,posti_totali,posti_disabili,prezzo_posti) VALUES('Dedalo','100','7','9') ")
conn.execute("INSERT INTO sale(nome,posti_totali,posti_disabili,prezzo_posti) VALUES('Icaro','200','3','7') ")
conn.execute("INSERT INTO sale(nome,posti_totali,posti_disabili,prezzo_posti) VALUES('Ulisse','50','1','12') ")
conn.execute("INSERT INTO sale(nome,posti_totali,posti_disabili,prezzo_posti) VALUES('Percy','150','5','8') " )

#GENERE
#creo i generi possibili che un film può avere
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


#REGISTA

conn.execute("INSERT INTO attori(nome,cognome,genere,stato,data_nascita,descr) VALUES('Bruce','Schetta','1','California','1914-10-10','Se el mejo tocco de oro') ")

#FILM
#creo i film
conn.execute("INSERT INTO film(titolo,autore,durata,generi,lingua_originale) VALUES('Io sono leggenda','1','145','1','1')" )
conn.execute("INSERT INTO film(titolo,autore,durata,generi,lingua_originale) VALUES('Transformers','1','200','1','1') ")
conn.execute("INSERT INTO film(titolo,autore,durata,generi,lingua_originale) VALUES('Alba','1','245','1','1') ")

#PROIEZIONI
#creo le proiezioni
conn.execute("INSERT INTO proiezioni(sala,film,data,ora,posti_liberi,posti_occupati) VALUES('1','1',DATE(NOW()),'20:00:00','98','2') ")
conn.execute("INSERT INTO proiezioni(sala,film,data,ora,posti_liberi,posti_occupati) VALUES('2','2',DATE(NOW()),'22:00:00','199','1') ")
conn.execute("INSERT INTO proiezioni(sala,film,data,ora,posti_liberi,posti_occupati) VALUES('3','3',DATE(NOW()),'18:00:00','49','1') ")
conn.execute("INSERT INTO proiezioni(sala,film,data,ora,posti_liberi,posti_occupati) VALUES('4','3',DATE(NOW()),'16:00:00','119','1') ")


#ACQUISTI
conn.execute("INSERT INTO acquisti(utente,proiezione,posti) VALUES('99','1','12')" )
conn.execute("INSERT INTO acquisti(utente,proiezione,posti) VALUES('99','1','14') ")
conn.execute("INSERT INTO acquisti(utente,proiezione,posti) VALUES('99','2','12')" )
conn.execute("INSERT INTO acquisti(utente,proiezione,posti) VALUES('99','3','12') ")
conn.execute("INSERT INTO acquisti(utente,proiezione,posti) VALUES('99','4','12')" )

#RUOLI
#creo due variabili che rispecchiano i due ruoli del mio database
role_gestore = "SELECT 1 FROM pg_roles WHERE rolname='gestore'"
role_cliente = "SELECT 1 FROM pg_roles WHERE rolname='cliente'"

#controllo se i due ruoli esistono già, li elimino e li ricreo nel caso siano state apportate modifiche
#nel caso non esistano già li creo
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


#GESTORE
#lista dei permessi che il gestore possiede: connettersi al database, utilizzo di tutte le tabelle e funzioni, di vedere tutte le tabelle e di modificarne molte
conn.execute("GRANT CONNECT ON DATABASE rossini TO gestore")
conn.execute("GRANT USAGE ON SCHEMA public TO gestore")
conn.execute("GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO gestore")
conn.execute("GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO gestore")
conn.execute("GRANT SELECT ON film, proiezioni, sale, acquisti, utenti ,attori ,generi, genere TO gestore;")
conn.execute("GRANT INSERT ON genere, generi, attori, film, sale, proiezioni TO gestore;")


#CLIENTE
#lista di permessi del cliente: connettersi al database, utilizzo delle tabelle, e visione
conn.execute("GRANT CONNECT ON DATABASE rossini TO cliente")
conn.execute("GRANT USAGE ON SCHEMA public TO cliente")
conn.execute("GRANT SELECT ON film, proiezioni, sale, acquisti, utenti ,attori ,generi, genere TO cliente;")
conn.execute("GRANT SELECT,INSERT,DELETE  ON TABLE public.acquisti TO cliente;")
conn.execute("GRANT UPDATE ON proiezioni TO cliente;")
conn.execute("GRANT SELECT ON SEQUENCE public.attori_idattori_seq , public.acquisti_id_seq TO cliente;")
conn.execute("GRANT UPDATE ON SEQUENCE public.acquisti_id_seq TO cliente;")
conn.execute("GRANT USAGE ON SEQUENCE public.acquisti_id_seq TO cliente;")
conn.execute("GRANT REFERENCES ON TABLE proiezioni,utenti TO gestore;")


#conn.execute("GRANT SELECT ON TABLE public.prezzi_sala_mat TO gestore;")
#conn.execute("GRANT TRIGGER ON TABLE public.prezzi_sala_mat TO cliente;")
#conn.execute("GRANT EXECUTE ON FUNCTION public.refresh_prezzi_sala_mat() TO cliente;")
#conn.execute("GRANT TRIGGER ON TABLE public.prezzi_sala_mat TO cliente;")



#chiudo la connessione al mio database
conn.close()
#creo una connessione al mio engine e creo delle materialized view che utilizzo per alcune query della pagina statistiche del gestore
conn = engine_gestore.connect()
conn.execute("CREATE MATERIALIZED VIEW prezzi_sala_mat (film, incasso, sala, data ) AS SELECT f.codfilm, SUM(p.posti_occupati)*s.prezzo_posti AS incasso, s.nome , p.data FROM proiezioni p JOIN film f ON (p.film = f.codfilm) JOIN sale s ON(p.sala = s.nsala) GROUP BY s.nsala, f.codfilm , p.data")
conn.execute("CREATE MATERIALIZED VIEW prezzi_generi_mat (genere, incasso , sala, data ) AS SELECT g1.titolo, SUM(p.posti_occupati)*s.prezzo_posti, s.nome , p.data AS incasso FROM proiezioni p JOIN film f ON (p.film = f.codfilm) JOIN sale s ON(p.sala = s.nsala) JOIN generi g ON(f.generi = g.idgeneri) JOIN genere g1 ON (g.genere1 = g1.idgenere) GROUP BY s.nsala, g1.idgenere , p.data")
conn.execute("CREATE MATERIALIZED VIEW acquisti_utenti (utente, acquisti, data) AS SELECT u.id, COUNT(*), p.data FROM utenti u JOIN acquisti a ON (u.id = a.utente) JOIN proiezioni p ON(p.idproiezione = a.proiezione) GROUP BY u.id, p.data")
conn.close()
