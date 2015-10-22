#!flask/bin/python

from flask import Flask
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from models import *


def create_app():
    from colorama import init
    init()
    from config import add_configs
    app = add_configs(Flask(__name__))

    from sqlalchemy_utils.functions import database_exists, create_database
    if not database_exists(app.config.get('SQLALCHEMY_DATABASE_URI')):
        create_database(app.config.get('SQLALCHEMY_DATABASE_URI'), encoding='utf8')

    with app.app_context():
        from models import db

        db.init_app(app)
        app.db = db

        from models.oauth2 import oauth2_provider
        oauth2_provider.init_app(app)

        # import models
        Migrate(app, db, directory='bin/migrations/')

        mgr = Manager(app)
        mgr.add_command('db', MigrateCommand)

    return mgr


manager = create_app()

if __name__ == '__main__':
    manager.run()
