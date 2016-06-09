from datetime import datetime

from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseMixin(object):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column('created_at', db.DateTime, nullable=False,
                           default=datetime.now)
    updated_at = db.Column('updated_at', db.DateTime, nullable=False,
                           default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<{self.__class__.__name__}:{self.id}>'.format(self=self)


class CommentMixin(BaseMixin):
    text = db.Column(db.UnicodeText)
    is_active = db.Column(db.Boolean())


class PostMixin(BaseMixin):
    title = db.Column(db.Unicode)
    text = db.Column(db.UnicodeText)
    is_active = db.Column(db.Boolean())