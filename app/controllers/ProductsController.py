__author__ = 'gia'

from flask import request
from controllers import BaseController
from flask_restful import Resource, abort
from flask import current_app as app


class ProductsController(Resource, BaseController):
    @app.oauth.require_oauth('email')
    def get(self, q=None):
        return 'Hello world!!!'

    @app.oauth.require_oauth('email')
    def put(self, id):
        abort(404, message="Method PUT is not implemented")

    @app.oauth.require_oauth('email')
    def post(self):
        abort(404, message="Method POST is not implemented")
