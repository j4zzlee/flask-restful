__author__ = 'gia'

from flask import request
from controllers.apis import BaseApi
from flask_restful import Resource, abort, reqparse
from flask import current_app as app, jsonify
import string


class ProductsController(Resource, BaseApi):
    _resource_name = 'products'

    @app.oauth.require_oauth('email')
    def get(self, q=None):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'id',
            help='ID of product',
            required=True,
            location=['args']
        )

        args = parser.parse_args()
        return 'Hello world!!!'

    @app.oauth.require_oauth('email')
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

    @app.oauth.require_oauth('email')
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
