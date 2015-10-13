__author__ = 'gia'

from flask import request, current_app as app
from flask_restful import Resource, abort
from controllers import BaseController


class CategoriesController(Resource, BaseController):
    @app.oauth.require_oauth('email')
    def get(self, q=None):
        return 'Hello world!!!'
