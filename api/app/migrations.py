#!flask/bin/python

from flask import Flask
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from models import *


def create_app():
    from config import add_configs
    app = add_configs(Flask(__name__))

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
