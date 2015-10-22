__author__ = 'gia'
__all__ = ['oauth2_provider']

from libraries.oauth2 import OAuthProviderImpl
from datetime import datetime, timedelta


class OAuth2Provider(OAuthProviderImpl):
    def _clientgetter(self, client_id):
        from models import Client
        return Client.query.filter_by(client_id=client_id).first()

    def _grantgetter(self, client_id, code):
        from models import Grant
        return Grant.query.filter_by(client_id=client_id, code=code).first()

    def _grantsetter(self, client_id, code, req, *args, **kwargs):
        import uuid
        from models import Grant
        # decide the expires time yourself
        expires = datetime.utcnow() + timedelta(days=1)
        grant = Grant(
            id=str(uuid.uuid4()),
            client_id=client_id,
            code=code['code'],
            redirect_uri=req.redirect_uri,
            _scopes=' '.join(req.scopes),
            user=req.client.user_id if req and req.client else None,
            expires=expires
        )

        from flask import current_app as app
        session = app.db.session
        session.add(grant)
        session.commit()
        return grant

    def _tokengetter(self, access_token=None, refresh_token=None):
        from models import Token
        if access_token:
            return Token.query.filter_by(access_token=access_token).first()
        elif refresh_token:
            return Token.query.filter_by(refresh_token=refresh_token).first()

    def _tokensetter(self, token, req, *args, **kwargs):
        from models import Token
        from flask import current_app as app
        session = app.db.session
        if req.user:
            toks = req.user and Token.query.filter_by(
                client_id=req.client.client_id,
                user_id=req.user.id) or Token.query.filter_by(client_id=req.client.client_id)
            # make sure that every client has only one token connected to a user
            for t in toks:
                session.delete(t)

        expires_in = token.get('expires_in')
        expires = datetime.utcnow() + timedelta(seconds=expires_in)

        tok = Token(
            access_token=token['access_token'],
            refresh_token=token['refresh_token'],
            token_type=token['token_type'],
            _scopes=token['scope'],
            expires=expires,
            client_id=req.client.client_id,
            user_id=req.user and req.user.id or None,
        )
        session.add(tok)
        session.commit()
        return tok

    def _usergetter(self, username, password, *args, **kwargs):
        from models.User import User
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None


oauth2_provider = OAuth2Provider()
