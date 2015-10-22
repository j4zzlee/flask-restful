__author__ = 'gia'

from models import Base, EntityBase, db
from libraries.db import guid


class Product(db.Model, Base, EntityBase):
    __tablename__ = 'product'
    id = db.Column(guid(), primary_key=True)

    # Relationships with Category
    category_id = db.Column(guid(), db.ForeignKey(
        'category.id',
        name='fk_product_id_category',
        onupdate='CASCADE',
        ondelete='CASCADE'
    ), index=True)
    category = db.relationship('Category')

    name = db.Column(db.String(255), nullable=False)
    photo = db.Column(db.String(255))
    code = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.Text)

    @property
    def entity_type(self):
        return EntityBase.TYPE_PRODUCT

    @property
    def resource_type(self):
        from models.acl import AclResource
        return AclResource.PRODUCT
