__author__ = 'gia'

from flask import request
from controllers.apis import BaseApi
from flask_restful import Resource, abort, reqparse
from models.oauth2 import oauth2_provider as oauth


class ProductsController(Resource, BaseApi):
    _resource_name = 'products'

    @oauth.require_oauth('email')
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'id',
            help='ID of product',
            location=['args']
        )
        parser.add_argument(
            'category_id',
            help='ID of category',
            location=['args']
        )
        parser.add_argument(
            'from_price',
            help='Lowest price',
            location=['args']
        )
        parser.add_argument(
            'to_price',
            help='Highest price',
            location=['args']
        )
        parser.add_argument(
            'size',
            help='Items per page',
            location=['args']
        )
        parser.add_argument(
            'page',
            help='Offset page',
            location=['args']
        )

        args = parser.parse_args()

        from models.Product import Product
        from sqlalchemy import and_, or_

        page = args.get('page') or 0
        size = args.get('size') or 20

        products = Product.query
        if args.get('id'):
            products = products.filter_by(id=args.get('id'))

        # if args.get('category_id'):
        #     products = products.filter(or_(
        #
        #     ))

        if args.get('from_price'):
            products = products.filter(Product.price >= args.get('from_price'))

        if args.get('to_price'):
            products = products.filter(Product.price <= args.get('to_price'))

        return {
            "total": products.count(),
            "page": page,
            "size": size,
            "items": self.make_response(products.limit(size).offset(page * size).all())
        }

    @oauth.require_oauth('email')
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'id',
            help='ID of product',
            required=True,
            location=['values', 'json']
        )
        args = parser.parse_args()
        abort(404, message="Method PUT is not implemented")

    @oauth.require_oauth('email')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'id',
            help='ID of product',
            required=True,
            location=['values', 'json']
        )
        args = parser.parse_args()
        abort(404, message="Method POST is not implemented")

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'id',
            help='ID of product',
            required=True,
            location=['values', 'json']
        )
        args = parser.parse_args()
        abort(404, message="Method DELETE is not implemented")
