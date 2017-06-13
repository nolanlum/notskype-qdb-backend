import binascii
from functools import wraps

import connexion
from flask import abort, g
from oauth2client import client, crypt

import qdb


def google_authenticate(f):
    @wraps(f)
    def _wrapper(*args, **kwargs):
        if not qdb.AUTH_ENABLED:
            g.user = {'given_name': 'Anonymous', 'email': 'anonymous@esports.moe'}
            return f(*args, **kwargs)

        google_token = connexion.request.headers.get('X-Google-Token')
        if not google_token:
            abort(403)

        try:
            idinfo = client.verify_id_token(google_token, qdb.CLIENT_ID)
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError('Wrong issuer.')

            if idinfo.get('email') not in qdb.AUTHORIZED_USERS:
                raise crypt.AppIdentityError('User not authorized.')

            g.user = idinfo

            return f(*args, **kwargs)
        except crypt.AppIdentityError:
            abort(403)
        except binascii.Error:
            abort(400)

    return _wrapper


def post(slack_token):
    pass
