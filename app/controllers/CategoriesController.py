__author__ = 'gia'

from flask import request
from flask_restful import Resource


class CategoriesController(Resource):
    def get(self, q=None):
        return {
            'hello': 'GET METHOD'
        }

    def put(self):
        return NotImplementedError('The PUT method is not implemented', 404)

    def post(self):
        return NotImplementedError('The POST method is not implemented', 404)
