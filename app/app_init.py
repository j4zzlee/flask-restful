#!flask/bin/python
from flask import Flask, request, render_template, Blueprint
from controllers import ApiProvider
from OAuth2 import OAuthProviderImpl
from flask_sqlalchemy import SQLAlchemy

oauth = OAuthProviderImpl()
db = SQLAlchemy()


def create_app():
    global app
    global db
    global migrate
    global manager
    global oauth_controller

    app = Flask(__name__)
    app.config.from_object('config.default')
    app.config.from_object('config.production')

    try:
        # only get configs from local if exists
        app.config.from_object('config.local')
    except ImportError:
        pass

    app.register_blueprint(oauth_controller)

    db.init_app(app)

    oauth.init_app(app)

    api = ApiProvider(app, decorators=[oauth.require_oauth('email')])
    api.add_controllers()

    return app


oauth_controller = Blueprint('oauth', __name__, url_prefix='/oauth')


@oauth_controller.route('/authorize', methods=['GET', 'POST'])
@oauth.authorize_handler
def authorize(*args, **kwargs):
    return True


@oauth_controller.route('/token', methods=['POST'])
@oauth.token_handler
def access_token():
    return {'version': '0.1.0'}


@oauth_controller.route('/revoke', methods=['POST'])
@oauth.revoke_handler
def revoke_token(): pass

# This should be on last line of this file
app = create_app()

@app.route('/application/authorized', methods=['GET'])
def authorized(*args, **kwargs):
    from flask import jsonify
    return jsonify({
        'code': request.values.get('code', '')
    })


@app.errorhandler(Exception)
def handle_invalid_usage(error):
    from flask import jsonify

    response = jsonify({
        'error': hasattr(error, 'error') and error.error or 'Unexpected Error!!!',
        'error_description': hasattr(error,
                                     'description') and error.description or
                             'The system has encountered an unexpected error. Please contact administrator (hoanggia.lh@gmail.com) for better supports',
        'message': error.message,
        'status_code': hasattr(error, 'status_code') and error.status_code or 500,
    })

    response.status_code = hasattr(error, 'status_code') and error.status_code or 500
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
