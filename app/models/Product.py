__author__ = 'gia'

from models import Base, guid, EntityBase, db


class Product(db.Model, Base, EntityBase):
    __tablename__ = 'product'
    id = db.Column(guid(), primary_key=True)

    # Relationships with Category
    category_id = db.Column(guid(), db.ForeignKey('category.id', name='fk_product_category_id_category'), index=True)
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
