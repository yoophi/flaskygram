from flask.ext.admin.contrib import sqla

from . import admin
from ..models import db, User, Role, Client, Token, Todo

admin.add_view(sqla.ModelView(User, session=db.session, name='User'))
admin.add_view(sqla.ModelView(Role, session=db.session, name='Role'))
admin.add_view(sqla.ModelView(Client, session=db.session, name='Client'))
admin.add_view(sqla.ModelView(Token, session=db.session, name='Token'))
admin.add_view(sqla.ModelView(Todo, session=db.session, name='Todo'))
