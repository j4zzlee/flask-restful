#!flask/bin/python

from flask import Flask
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand


def create_app():
    from config import add_configs
    app = add_configs(Flask(__name__))

    with app.app_context():
        from models import db
        from models.Category import Category
        from models.EntityMeta import EntityMeta
        from models.MetaGroup import MetaGroup
        from models.MetaValue import MetaValue
        from models.Product import Product

        db.init_app(app)
        app.db = db

        # import models
        migrate = Migrate(app, db, directory='bin/migrations/')

        mgr = Manager(app)
        mgr.add_command('db', MigrateCommand)

    return mgr


manager = create_app()

if __name__ == '__main__':
    manager.run()
