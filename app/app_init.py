#!flask/bin/python
from flask import Flask, request, render_template, Blueprint
from controllers import ApiProvider
from OAuth2 import OAuthProviderImpl
from flask_sqlalchemy import SQLAlchemy

oauth = OAuthProviderImpl()
db = SQLAlchemy()


def create_app():
    global app
    global migrate
    global manager
    global oauth_controller

    app = Flask(__name__)
    app.config.from_object('config')

    app.register_blueprint(oauth_controller)

    db.init_app(app)

    oauth.init_app(app)

    # api = ApiProvider(app, decorators=[oauth.require_oauth('email')])
    # api.add_controllers()

    return app


oauth_controller = Blueprint('oauth', __name__, url_prefix='/oauth')


@oauth_controller.route('/errors', methods=['GET', 'POST'])
def errors(*args, **kwargs):
    from flask import jsonify
    return jsonify(request.args)


@oauth_controller.route('/authorize', methods=['GET', 'POST'])
@oauth.authorize_handler
def authorize(*args, **kwargs):
    from models import Client
    if request.method == 'GET':
        client_id = kwargs.get('client_id')
        client = Client.query.filter_by(client_id=client_id).first()
        kwargs['client'] = client
        return render_template('oauthorize.html', **kwargs)

    confirm = request.form.get('confirm', 'no')
    return confirm == 'yes'


@oauth_controller.route('/token', methods=['POST'])
@oauth.token_handler
def access_token():
    return {'version': '0.1.0'}


@oauth_controller.route('/revoke', methods=['POST'])
@oauth.revoke_handler
def revoke_token(): pass


# This should be on last line of this file
app = create_app()


@app.errorhandler(Exception)
def handle_invalid_usage(error):
    from flask import jsonify

    response = jsonify({
        'error': error.error,
        'error_description': error.description,
        'message': error.message,
        'status_code': error.status_code,
    })

    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
