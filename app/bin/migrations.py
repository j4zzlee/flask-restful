#!flask/bin/python

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

db = SQLAlchemy()


def create_app():
    global app
    global migrate
    global manager
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    db.init_app(app)

    migrate = Migrate(app, db)

    manager = Manager(app)
    manager.add_command('db', MigrateCommand)

    return app


app = create_app()


if __name__ == '__main__':
    manager.run()
