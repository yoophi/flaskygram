#!/usr/bin/env python
# coding: utf-8

"""
sqlalchemy model
"""
from datetime import datetime
from flask.ext.security import RoleMixin, UserMixin
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, synonym

db = SQLAlchemy()

# Define models
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))


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


class Role(db.Model, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<{self.__class__.__name__}:{self.name}>'.format(self=self)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    current_login_at = db.Column(db.DateTime())
    current_login_ip = db.Column(db.String(255))
    login_count = db.Column(db.Integer)

    def __repr__(self):
        return '<{self.__class__.__name__}:{self.email}>'.format(self=self)


class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(40))

    # human readable description, not required
    description = db.Column(db.Unicode(400))

    # creator of the client, not required
    user_id = db.Column(
        db.Integer,
        ForeignKey('users.id'),
        nullable=False,
    )
    user = relationship('User')

    client_id = db.Column(db.Unicode(40), unique=True)
    client_secret = db.Column(db.Unicode(55), index=True, nullable=False)

    # public or confidential
    is_confidential = db.Column(db.Boolean)

    redirect_uris_text = db.Column(db.UnicodeText)
    default_scopes_text = db.Column(db.UnicodeText)

    @property
    def client_type(self):
        if self.is_confidential:
            return 'confidential'
        return 'public'

    @property
    def redirect_uris(self):
        if self.redirect_uris_text:
            return self.redirect_uris_text.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        if self.default_scopes_text:
            return self.default_scopes_text.split()
        return []

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)


class Grant(db.Model):
    __tablename__ = 'grants'

    id = db.Column(db.Integer, primary_key=True)

    # user_id = db.Column(db.Unicode(200))dd
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
    )
    user = relationship('User')

    client_id = db.Column(
        db.Unicode(40),
        db.ForeignKey('clients.client_id'),
        nullable=False,
    )
    client = relationship('Client')

    code = db.Column(db.Unicode(255), index=True, nullable=False)

    redirect_uri = db.Column(db.Unicode(255))
    expires = db.Column(db.DateTime)

    _scopes = db.Column(db.UnicodeText)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []


class Token(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(
        db.Unicode(40),
        db.ForeignKey('clients.client_id'),
        nullable=False,
    )
    client = relationship('Client')

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False,
    )
    user = relationship('User')

    # currently only bearer is supported
    token_type = db.Column(db.Unicode(40))

    access_token = db.Column(db.Unicode(255), unique=True)
    refresh_token = db.Column(db.Unicode(255), unique=True)
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.UnicodeText)

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []

    def _get_scope(self):
        if self._scopes:
            return self._scopes.split()
        return []

    def _set_scope(self, scope):
        if scope:
            scope = scope
        self._scopes = scope

    scope_descriptor = property(_get_scope, _set_scope)
    scope = synonym('_scopes', descriptor=scope_descriptor)

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.id}>'.format(self=self)


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


class Tag(db.Model, BaseMixin):
    __tablename__ = 'tags'


class PostComment(db.Model, CommentMixin):
    __tablename__ = 'post_comments'

    post_id = db.Column(db.Integer, ForeignKey('posts.id'), nullable=False, )
    post = relationship('Post', backref='comments')

    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False, )
    user = relationship('User', backref='media_comments')


class Relationship(db.Model, BaseMixin):
    __tablename__ = 'relationships'
    __table_args__ = (
        (UniqueConstraint("user_id", "followed_by_id", name="unique_idx_user_id_followed_by_id")),
    )

    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    followed_by_id = db.Column(db.Integer, ForeignKey('users.id'))

    user = relationship('User', foreign_keys=user_id, backref='followed_by')
    followed_by = relationship('User', foreign_keys=followed_by_id, backref='follows')

    def __repr__(self):
        return u'<{self.__class__.__name__}: {self.followed_by_id} to {self.user_id}>'.format(self=self)
