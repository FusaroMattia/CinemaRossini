from flask_login import UserMixin,AnonymousUserMixin
from flask_user import UserMixin
from . import db
from .models import User,Role,UserRoles



Gestore = Role(name='Gestore')
Cliente = Role(name='Cliente')
global Gestore
global Cliente

db.session.commit()
