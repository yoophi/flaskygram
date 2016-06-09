from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from flaskygram.database import db, BaseMixin


class Media(db.Model, BaseMixin):
    __tablename__ = 'media'

    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False, )
    user = relationship('User', backref='media')

    post_id = db.Column(
        db.Integer,
        ForeignKey('posts.id'),
        nullable=True,
    )
    post = relationship('Post', backref='media')

    name = db.Column(db.Unicode)
    filename = db.Column(db.Unicode)
    filesize = db.Column(db.Integer)
    mimetype = db.Column(db.Unicode)
    dir = db.Column(db.Unicode)
    shortcode = db.Column(db.Unicode)