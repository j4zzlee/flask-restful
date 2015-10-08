__author__ = 'gia'

from flask import request
from flask_restful import Resource, abort


class ProductsController(Resource):
    def get(self, q=None):
        return 'Hello world!!!'

    def put(self):
        abort(404, message="Method PUT is not implemented")

    def post(self):
        abort(404, message="Method POST is not implemented")
