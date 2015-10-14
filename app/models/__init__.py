__author__ = 'gia'
__all__ = ['Category', 'EntityMeta', 'MetaGroup', 'MetaValue', 'Product', 'User']

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
import uuid

db = SQLAlchemy()

"""
@:type flask_sqlalchemy.SQLAlchemy
"""


class guid(TypeDecorator):
    """Platform-independent GUID type.

    Uses Postgresql's UUID type, otherwise uses
    CHAR(32), storing as stringified hex values.

    """
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value)
            else:
                # hexstring
                return "%.32x" % value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(value)


class Base:
    def __init__(self):
        pass

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class EntityBase:
    TYPE_USER = 1
    TYPE_PRODUCT = 2
    TYPE_CATEGORY = 4

    def __init__(self):
        pass

    def entity_type(self):
        return None

    @property
    def properties(self):
        # return None
        from sqlalchemy import and_
        from models.EntityMeta import EntityMeta
        return EntityMeta.query.filter(and_(
            EntityMeta.entity_id == getattr(self, 'id'),
            EntityMeta.entity_type.op('&')(self.entity_type()) > 0
        ))


class Client(db.Model, Base):
    __tablename__ = 'client'
    # human readable name, not required
    name = db.Column(db.String(40))

    # human readable description, not required
    description = db.Column(db.String(400))

    # creator of the client, not required
    user_id = db.Column(db.ForeignKey('user.id'))
    from models.User import User
    # required if you need to support client credential
    user = db.relationship(User)

    client_id = db.Column(db.String(40), primary_key=True)
    client_secret = db.Column(db.String(55), unique=True, index=True,
                              nullable=False)

    # public or confidential
    is_confidential = db.Column(db.Boolean)

    _redirect_uris = db.Column(db.Text)
    _default_scopes = db.Column(db.Text)

    @property
    def client_type(self):
        if self.is_confidential:
            return 'confidential'
        return 'public'

    @property
    def redirect_uris(self):
        if self._redirect_uris:
            return self._redirect_uris.split()
        return []

    @property
    def default_redirect_uri(self):
        return self.redirect_uris[0]

    @property
    def default_scopes(self):
        return [
            'email'
        ]
        # if self._default_scopes:
        #     return self._default_scopes.split()
        # return []


class Grant(db.Model, Base):
    __tablename__ = 'grant'
    id = db.Column(db.String(40), primary_key=True)

    user_id = db.Column(
        guid(), db.ForeignKey('user.id', ondelete='CASCADE')
    )

    from models.User import User
    user = db.relationship(User)

    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id'),
        nullable=False,
    )
    client = db.relationship('Client')

    code = db.Column(db.String(255), index=True, nullable=False)

    redirect_uri = db.Column(db.String(255))
    expires = db.Column(db.DateTime)

    _scopes = db.Column(db.Text)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []

    def validate_redirect_uri(self, redirect_uri):
        return True


class Token(db.Model, Base):
    __tablename__ = 'token'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(
        db.String(40), db.ForeignKey('client.client_id'),
        nullable=False,
    )
    client = db.relationship('Client')

    user_id = db.Column(
        guid(), db.ForeignKey('user.id')
    )
    user = db.relationship('User')

    # currently only bearer is supported
    token_type = db.Column(db.String(40))

    access_token = db.Column(db.String(255), unique=True)
    refresh_token = db.Column(db.String(255), unique=True)
    expires = db.Column(db.DateTime)
    _scopes = db.Column(db.Text)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @property
    def scopes(self):
        if self._scopes:
            return self._scopes.split()
        return []
