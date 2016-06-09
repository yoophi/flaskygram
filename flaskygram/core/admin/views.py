from flask.ext.admin.contrib import sqla

from . import admin
from ..models import User, Token, Media, Relationship, Tag, PostComment
from flaskygram.modules.models import Post, Media, Tag, PostComment
from flaskygram.core.api_1_0.models import Client, Token
from flaskygram.core.accounts.models import Role, User, Relationship
from flaskygram.database import db


#
admin.add_view(sqla.ModelView(Media, session=db.session, name='Media', category='Media'))
admin.add_view(sqla.ModelView(Post, session=db.session, name='Post', category='Media'))
admin.add_view(sqla.ModelView(PostComment, session=db.session, name='PostComment', category='Media'))
admin.add_view(sqla.ModelView(Tag, session=db.session, name='Tag', category='Media'))

#

#
admin.add_view(sqla.ModelView(Client, session=db.session, name='Client', category='System'))
admin.add_view(sqla.ModelView(Token, session=db.session, name='Token', category='System'))
