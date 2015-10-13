__author__ = 'gia'

api_version = '1.0'


def add_apis(app, api):
    with app.app_context():
        from controllers.ProductsController import ProductsController
        api.add_resource(ProductsController, '/api/v{0}/products'.format(api_version))

        from controllers.CategoriesController import CategoriesController
        api.add_resource(CategoriesController, '/api/v{0}/categories'.format(api_version))


from flask import abort


class BaseController:
    def __init__(self):
        pass

    def get(self, q=None):
        abort(404, message="Method GET is not implemented")

    def put(self, id):
        abort(404, message="Method PUT is not implemented")

    def post(self):
        abort(404, message="Method POST is not implemented")

    def delete(self, id):
        abort(404, message="Method DELETE is not implemented")
