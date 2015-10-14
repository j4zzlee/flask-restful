__author__ = 'gia'
from models import Base, guid, EntityBase, db


class Category(db.Model, Base, EntityBase):
    __tablename__ = 'category'
    id = db.Column(guid(), primary_key=True)

    # Relationship with parent Category
    parent_id = db.Column(guid(), db.ForeignKey('category.id', name='fk_category_category_id_category'), index=True)
    parent = db.relationship(lambda: Category, remote_side=id, backref='sub_products')

    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(255))

    @property
    def entity_type(self):
        return EntityBase.TYPE_CATEGORY
