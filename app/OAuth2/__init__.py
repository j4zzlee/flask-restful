__author__ = 'gia'

import logging
from functools import wraps
from flask_oauthlib.provider import OAuth2Provider
from datetime import datetime, timedelta
from flask import request
from oauthlib import oauth2
from flask_oauthlib.utils import extract_params, create_response

log = logging.getLogger('flask_oauthlib')


class OAuthProviderImpl(OAuth2Provider):
    def _clientgetter(self, client_id):
        from models import Client
        return Client.query.filter_by(client_id=client_id).first()

    def _grantgetter(self, client_id, code):
        from models import Grant
        return Grant.query.filter_by(client_id=client_id, code=code).first()

    def _grantsetter(self, client_id, code, request, *args, **kwargs):
        import uuid
        from app_init import db
        from models import Grant

        # decide the expires time yourself
        expires = datetime.utcnow() + timedelta(days=1)
        grant = Grant(
            id=str(uuid.uuid4()),
            client_id=client_id,
            code=code['code'],
            redirect_uri=request.redirect_uri,
            _scopes=' '.join(request.scopes),
            user=self.get_current_user(),
            expires=expires
        )
        db.session.add(grant)
        db.session.commit()
        return grant

    def _tokengetter(self, access_token=None, refresh_token=None):
        from models import Token
        if access_token:
            return Token.query.filter_by(access_token=access_token).first()
        elif refresh_token:
            return Token.query.filter_by(refresh_token=refresh_token).first()

    def _tokensetter(self, token, request, *args, **kwargs):
        from models import Token
        from app_init import db

        if request.user:
            toks = request.user and Token.query.filter_by(
                client_id=request.client.client_id,
                user_id=request.user.id) or Token.query.filter_by(client_id=request.client.client_id)
            # make sure that every client has only one token connected to a user
            for t in toks:
                db.session.delete(t)

        expires_in = token.get('expires_in')
        expires = datetime.utcnow() + timedelta(seconds=expires_in)

        tok = Token(
            access_token=token['access_token'],
            refresh_token=token['refresh_token'],
            token_type=token['token_type'],
            _scopes=token['scope'],
            expires=expires,
            client_id=request.client.client_id,
            user_id=request.user and request.user.id or None,
        )
        db.session.add(tok)
        db.session.commit()
        return tok

    def _usergetter(self, username, password, *args, **kwargs):
        from models import User
        user = User.query.filter_by(username=username).first()
        if user.check_password(password):
            return user
        return None

    def get_current_user(self):
        return None

    def authorize_handler(self, f):
        """Authorization handler decorator.

        This decorator will sort the parameters and headers out, and
        pre validate everything::

            @app.route('/oauth/authorize', methods=['GET', 'POST'])
            @oauth.authorize_handler
            def authorize(*args, **kwargs):
                if request.method == 'GET':
                    # render a page for user to confirm the authorization
                    return render_template('oauthorize.html')

                confirm = request.form.get('confirm', 'no')
                return confirm == 'yes'
        """

        @wraps(f)
        def decorated(*args, **kwargs):
            # raise if server not implemented
            server = self.server
            uri, http_method, body, headers = extract_params()

            if request.method in ('GET', 'HEAD'):
                redirect_uri = request.args.get('redirect_uri', self.error_uri)
                log.debug('Found redirect_uri %s.', redirect_uri)
                try:
                    ret = server.validate_authorization_request(
                        uri, http_method, body, headers
                    )
                    scopes, credentials = ret
                    kwargs['scopes'] = scopes
                    kwargs.update(credentials)
                except oauth2.FatalClientError as e:
                    log.debug('Fatal client error %r', e)
                    raise
                except oauth2.OAuth2Error as e:
                    log.debug('OAuth2Error: %r', e)
                    raise

            else:
                redirect_uri = request.values.get(
                    'redirect_uri', self.error_uri
                )

            try:
                rv = f(*args, **kwargs)
            except oauth2.FatalClientError as e:
                log.debug('Fatal client error %r', e)
                raise
            except oauth2.OAuth2Error as e:
                log.debug('OAuth2Error: %r', e)
                raise

            if not isinstance(rv, bool):
                # if is a response or redirect
                return rv

            if not rv:
                # denied by user
                e = oauth2.AccessDeniedError()
                # return redirect(e.in_uri(redirect_uri))
                raise oauth2.OAuth2Error('You are not allowed to perform this action')
            return self.confirm_authorization_request()

        return decorated

    def confirm_authorization_request(self):
        """When consumer confirm the authorization."""
        server = self.server
        scopes = request.args.get('scopes', 'email').split()
        credentials = dict(
            client_id=request.values.get('client_id'),
            redirect_uri=request.values.get('redirect_uri', None),
            response_type=request.values.get('response_type', None),
            state=request.values.get('state', None)
        )
        log.debug('Fetched credentials from request %r.', credentials)
        redirect_uri = credentials.get('redirect_uri')
        log.debug('Found redirect_uri %s.', redirect_uri)

        uri, http_method, body, headers = extract_params()
        try:
            ret = server.create_authorization_response(
                uri, http_method, body, headers, scopes, credentials)
            log.debug('Authorization successful.')
            return create_response(*ret)
        except oauth2.FatalClientError as e:
            log.debug('Fatal client error %r', e)
            raise
        except oauth2.OAuth2Error as e:
            log.debug('OAuth2Error: %r', e)
            raise
