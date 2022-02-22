import time

from authlib.oauth2.rfc7662 import IntrospectionEndpoint as _IntrospectionEndpoint
from authlib.oauth2.rfc7009 import RevocationEndpoint as _RevocationEndpoint

from app.database import db
from app.models import Token


class IntrospectionEndpoint(_IntrospectionEndpoint):
    def query_token(self, token, token_type_hint, client=None):
        if token_type_hint == 'access_token':
            tok = db.session.query(Token).filter_by(access_token=token).first()
        elif token_type_hint == 'refresh_token':
            tok = db.session.query(Token).filter_by(refresh_token=token).first()
        else:
            # without token_type_hint
            tok = db.session.query(Token).filter_by(access_token=token).first()
            if not tok:
                tok = db.session.query(Token).filter_by(refresh_token=token).first()
        return tok

    def introspect_token(self, token):
        return {
            'active': True,
            'client_id': token.client_id,
            'token_type': token.token_type,
            'username': token.user.email,
            'scope': token.get_scope(),
            'sub': token.user.id,
            'aud': token.client_id,
            'iss': 'https://server.example.com/',
            'exp': token.expires_at,
            'iat': token.issued_at,
        }

    def check_permission(self, token, client, request):
        return True


class RevocationEndpoint(_RevocationEndpoint):
    def query_token(self, token, token_type_hint, client=None):
        if token_type_hint == 'access_token':
            tok = db.session.query(Token).filter_by(access_token=token).first()
        elif token_type_hint == 'refresh_token':
            tok = db.session.query(Token).filter_by(refresh_token=token).first()
        else:
            # without token_type_hint
            tok = db.session.query(Token).filter_by(access_token=token).first()
            if not tok:
                tok = db.session.query(Token).filter_by(refresh_token=token).first()
        return tok

    def revoke_token(self, token):
        token.revoked = True
        db.session.add(token)
        db.session.commit()
