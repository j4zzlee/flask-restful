#!flask/bin/python
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


def create_app():
    from config import add_configs
    # Register configurations
    application = add_configs(Flask(__name__))

    with application.app_context():
        # Register database (sqlalchemy)
        db = SQLAlchemy()
        db.init_app(application)
        application.db = db

        # Register OAuth2
        from OAuth2 import OAuthProviderImpl
        oauth = OAuthProviderImpl(application)
        application.oauth = oauth

        # Register BluePrints
        from controllers import add_blueprints
        add_blueprints(application)

        # Register Api
        from controllers import add_apis
        from flask_restful import Api
        add_apis(Api(application))

    return application


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
