__author__ = 'gia'

from flask import request
from models.oauth2 import oauth2_provider as oauth
from flask_restful import Resource, abort
from controllers.apis import BaseApi


class CategoriesController(Resource, BaseApi):
    _resource_name = 'categories'

    @oauth.require_oauth('email')
    def get(self):
        return 'Hello world!!!'
