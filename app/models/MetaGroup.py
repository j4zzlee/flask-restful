__author__ = 'gia'

from models import Base, db
from libraries.db import guid


class MetaGroup(db.Model, Base):
    __tablename__ = 'sys_meta_group'
    id = db.Column(guid(), primary_key=True)

    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
