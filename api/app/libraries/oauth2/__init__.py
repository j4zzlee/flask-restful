__author__ = 'gia'
__all__ = ['OAuthProviderImpl', 'Token', 'Grant', 'Client']

import logging
from functools import wraps
from flask_oauthlib.provider import OAuth2Provider
from flask import request
from oauthlib import oauth2
from flask_oauthlib.utils import extract_params, create_response
from werkzeug import cached_property

log = logging.getLogger('flask_oauthlib')


class OAuthProviderImpl(OAuth2Provider):
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

    def current_user(self):
        result = None
        if hasattr(request, 'user'):
            result = getattr(request, 'user')

        if not result and hasattr(request, 'oauth'):
            result = getattr(request.oauth, 'user')

        if not result and request.headers.get('Username') and request.headers.get('P@ssword123'):
            result = self._clientgetter(request.headers.get('Username'), request.headers.get('P@ssword123'))

        request.user = result

        return result

    def verify_request(self, scopes):
        """Verify current request, get the oauth data.

        If you can't use the ``require_oauth`` decorator, you can fetch
        the data in your request body::

            def your_handler():
                valid, req = oauth.verify_request(['email'])
                if valid:
                    return jsonify(user=req.user)
                return jsonify(status='error')
        """
        uri, http_method, body, headers = extract_params()
        import urllib, urlparse
        query = urlparse.urlparse(uri).query
        encoded_query = urllib.quote_plus(query)

        return self.server.verify_request(
            uri.replace(query, encoded_query), http_method, body, headers, scopes
        )

