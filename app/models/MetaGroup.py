__author__ = 'gia'

from flask import current_app as app
from models import Base, guid, db


class MetaGroup(db.Model, Base):
    __tablename__ = 'sys_meta_group'
    id = db.Column(guid(), primary_key=True)

    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
