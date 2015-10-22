__author__ = 'gia'
from models import Base, db
from libraries.db import guid


class EntityMeta(db.Model, Base):
    __tablename__ = 'sys_entity_meta'
    entity_id = db.Column(guid(), nullable=False, autoincrement=False, primary_key=True)
    entity_type = db.Column(db.Integer, nullable=False, autoincrement=False, primary_key=True)
    meta_id = db.Column(guid(), db.ForeignKey(
        'sys_meta_value.id',
        onupdate='CASCADE',
        ondelete='CASCADE'
    ), nullable=False, autoincrement=False, primary_key=True)
