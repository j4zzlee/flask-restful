__author__ = 'gia'

from flask import Blueprint
from models.oauth2 import oauth2_provider as oauth

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
