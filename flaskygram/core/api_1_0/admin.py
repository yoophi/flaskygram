from flask.ext.admin.contrib import sqla

from flaskygram.database import db
from flaskygram.extensions import admin
from .models import Token, Client

admin.add_view(sqla.ModelView(Client, session=db.session, name='Client', category='System'))
admin.add_view(sqla.ModelView(Token, session=db.session, name='Token', category='System'))
