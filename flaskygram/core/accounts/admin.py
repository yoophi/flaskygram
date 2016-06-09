from flask.ext.admin.contrib import sqla

from flaskygram.database import db
from flaskygram.extensions import admin
from .models import User, Role, Relationship

admin.add_view(sqla.ModelView(User, session=db.session, name='User', category='User'))
admin.add_view(sqla.ModelView(Role, session=db.session, name='Role', category='User'))
admin.add_view(sqla.ModelView(Relationship, session=db.session, name='Relationship', category='User'))
