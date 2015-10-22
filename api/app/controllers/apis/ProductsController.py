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
        u = oauth.current_user()
        from models.acl import AclResource, Privilege
        return {
            'Can view USER': u.is_allowed(AclResource.USER, Privilege.VIEW),
            'Can add USER': u.is_allowed(AclResource.USER, Privilege.ADD),
            'Can update USER': u.is_allowed(AclResource.USER, Privilege.UPDATE),
            'Can delete USER': u.is_allowed(AclResource.USER, Privilege.DELETE),
            'Can view ADMIN': u.is_allowed(AclResource.ADMIN, Privilege.VIEW),
            'Can view SETTINGS': u.is_allowed(AclResource.SETTINGS, Privilege.VIEW),
            'Can view PRODUCTS': u.is_allowed(AclResource.PRODUCT, Privilege.VIEW),
            'Can view CATEGORIES': u.is_allowed(AclResource.CATEGORY, Privilege.VIEW)
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
