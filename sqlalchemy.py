import sqlalchemy
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column("id", Integer , primary_key = True )
    name = Column ("name", String, unique = True )
    pwd = Column ("pwd",   String)

engine = create_engine('sqlite:///:memory', echo = True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind = engine)

session = Session()
user = User()
user.id = 0;
user.name = "tia"
user.pwd = "tia"

session.add(user)
session.commit()
session.close()


session = Session()

users = session.query(User).all()
for x in users:
    print("Username = %s and pwd = %s" % (x.name , x,pwd))

session.close()




