#!flask/bin/python

from flask import Flask
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.default')
    app.config.from_object('config.production')

    try:
        # only get configs from local if exists
        app.config.from_object('config.local')
    except ImportError:
        pass

    import models
    migrate = Migrate(app, models.db, directory='bin/migrations/')

    mgr = Manager(app)
    mgr.add_command('db', MigrateCommand)

    return mgr


manager = create_app()

if __name__ == '__main__':
    manager.run()
