__author__ = 'gia'

from flask import request, current_app as app
from flask_restful import Resource, abort
from controllers.apis import BaseApi


class CategoriesController(Resource, BaseApi):
    _resource_name = 'categories'

    @app.oauth.require_oauth('email')
    def get(self, q=None):
        return 'Hello world!!!'
