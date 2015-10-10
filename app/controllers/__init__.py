__author__ = 'gia'

from flask_restful import Api


api_version = '1.0'


class ApiProvider(Api):
    def add_controllers(self):
        from controllers.ProductsController import ProductsController
        self.add_resource(ProductsController, '/api/v{0}/products'.format(api_version))

        from controllers.CategoriesController import CategoriesController
        self.add_resource(CategoriesController, '/api/v{0}/categories'.format(api_version))
