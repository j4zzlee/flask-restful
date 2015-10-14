__author__ = 'gia'
from models import Base, guid, db


class EntityMeta(db.Model, Base):
    __tablename__ = 'sys_entity_meta'
    entity_id = db.Column(guid(), nullable=False, autoincrement=False, primary_key=True)
    entity_type = db.Column(db.Integer, nullable=False, autoincrement=False, primary_key=True)
    meta_id = db.Column(guid(), db.ForeignKey('sys_meta_value.id'), nullable=False, autoincrement=False,
                        primary_key=True)
