__author__ = 'gia'
from models import Base, guid, EntityBase, db


class User(db.Model, Base, EntityBase):
    __tablename__ = 'user'
    id = db.Column(guid(), primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    facebook = db.Column(db.String(255))
    skype = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    dob = db.Column(db.Integer())
    email = db.Column(db.String(255), unique=True, nullable=False)
    photo = db.Column(db.String(255))
    _password = db.Column(db.String(4000), name='password')
    about = db.Column(db.String(4000))

    @property
    def entity_type(self):
        return EntityBase.TYPE_USER

    @property
    def password(self):
        # No one should be able to find user's password
        return None

    @password.setter
    def password(self, password):
        from werkzeug.security import generate_password_hash
        self._password = generate_password_hash(password)

    def check_password_hash(self, password):
        from werkzeug.security import generate_password_hash
        return self._password == generate_password_hash(password)
