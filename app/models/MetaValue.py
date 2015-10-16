__author__ = 'gia'

from models import Base, db
from libraries.db import guid


class MetaValue(db.Model, Base):
    __tablename__ = 'sys_meta_value'

    TYPE_INFO = 1
    TYPE_LINK = 2

    id = db.Column(guid(), primary_key=True)

    group_id = db.Column(
        guid(),
        db.ForeignKey(
            'sys_meta_group.id',
            name='fk_sys_meta_value_id_sys_meta_group',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        index=True
    )
    group = db.relationship('MetaGroup')

    type = db.Column(db.Integer, default=1)
    name = db.Column(db.String(255), nullable=False, unique=True)
    value = db.Column(db.Text, nullable=False)
    link_to = db.Column(db.String(4000), default='#')
