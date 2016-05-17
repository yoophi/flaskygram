from flask.ext.admin.contrib import sqla

from . import admin
from ..models import db, User, Role, Client, Token, Media, Relationship, Tag, Post, PostComment

admin.add_view(sqla.ModelView(User, session=db.session, name='User', category='User'))
admin.add_view(sqla.ModelView(Role, session=db.session, name='Role', category='User'))

#
admin.add_view(sqla.ModelView(Media, session=db.session, name='Media', category='Media'))
admin.add_view(sqla.ModelView(Post, session=db.session, name='Post', category='Media'))
admin.add_view(sqla.ModelView(PostComment, session=db.session, name='PostComment', category='Media'))
admin.add_view(sqla.ModelView(Tag, session=db.session, name='Tag', category='Media'))

#
admin.add_view(sqla.ModelView(Relationship, session=db.session, name='Relationship', category='User'))

#
admin.add_view(sqla.ModelView(Client, session=db.session, name='Client', category='System'))
admin.add_view(sqla.ModelView(Token, session=db.session, name='Token', category='System'))
