#!flask/bin/python
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

from controllers.ProductsController import ProductsController
api.add_resource(ProductsController, '/products')

from controllers.CategoriesController import CategoriesController
api.add_resource(CategoriesController, '/categories')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
