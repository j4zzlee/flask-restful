__author__ = 'gia'

from flask import request
from controllers.apis import BaseApi
from flask_restful import Resource, abort, reqparse
from flask import jsonify
from models.oauth2 import oauth2_provider as oauth


class ProductsController(Resource, BaseApi):
    _resource_name = 'products'

    @oauth.require_oauth('email')
    def get(self, q=None):
        # parser = reqparse.RequestParser()
        # parser.add_argument(
        #     'id',
        #     help='ID of product',
        #     required=True,
        #     location=['args']
        # )
        #
        # args = parser.parse_args()

        # Current user
        # u = oauth.current_user()
        # return self.make_response(u)

        from models.Product import Product
        return self.make_response(Product.query.all())

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
