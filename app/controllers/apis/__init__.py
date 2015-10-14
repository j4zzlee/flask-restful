__author__ = 'gia'

from flask import abort


class BaseApi:
    _resource_name = ''

    def __init__(self):
        pass

    def get(self, q=None):
        abort(404, message="Method GET is not implemented")

    def put(self):
        abort(404, message="Method PUT is not implemented")

    def post(self):
        abort(404, message="Method POST is not implemented")

    def delete(self):
        abort(404, message="Method DELETE is not implemented")
