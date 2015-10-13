__author__ = 'gia'


def add_blueprints(app):
    from flask import Blueprint
    oauth_controller = Blueprint('oauth', __name__, url_prefix='/oauth')

    @oauth_controller.route('/authorize', methods=['GET', 'POST'])
    @app.oauth.authorize_handler
    def authorize(*args, **kwargs):
        return True

    @oauth_controller.route('/token', methods=['POST'])
    @app.oauth.token_handler
    def access_token():
        return {'version': '0.1.0'}

    @oauth_controller.route('/revoke', methods=['POST'])
    @app.oauth.revoke_handler
    def revoke_token(): pass

    app.register_blueprint(oauth_controller)
