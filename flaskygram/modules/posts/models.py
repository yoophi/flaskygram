from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from flaskygram.database import db, BaseMixin, CommentMixin


class Post(db.Model, BaseMixin):
    __tablename__ = 'posts'

    title = db.Column(db.String(255), unique=True)
    text = db.Column(db.UnicodeText, default=False)

    user_id = db.Column(
        db.Integer,
        ForeignKey('users.id'),
        nullable=False,
    )
    user = relationship('User', backref='todos')

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)


class PostComment(db.Model, CommentMixin):
    __tablename__ = 'post_comments'

    post_id = db.Column(db.Integer, ForeignKey('posts.id'), nullable=False, )
    post = relationship('Post', backref='comments')

    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False, )
    user = relationship('User', backref='media_comments')