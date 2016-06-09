from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, synonym

from flaskygram.database import db


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