from functools import wraps
from typing import Any, Callable, NamedTuple

import connexion
import requests
from cryptography.fernet import Fernet, InvalidToken
from flask import g, abort
from requests.auth import HTTPBasicAuth

import qdb


def slack_authenticate(f: Callable) -> Callable:
    @wraps(f)
    def _wrapper(*args: Any, **kwargs: Any) -> Any:
        if not qdb.AUTH_ENABLED:
            return f(*args, **kwargs)

        qdb_token = connexion.request.headers.get('X-Qdb-Token', as_bytes=True)
        if not qdb_token:
            return abort(403)

        try:
            g.access_token = Fernet(qdb.SECRET_KEY).decrypt(qdb_token)
        except InvalidToken:
            return abort(403)

        return f(*args, **kwargs)

    return _wrapper


class SlackUser(NamedTuple):
    id: str
    name: str
    email: str


ANONYMOUS_USER = SlackUser(id='UANONANON', name='Anonymous', email='anonymous@esports.moe')


def fetch_slack_identity() -> SlackUser:
    if not g.access_token:
        return ANONYMOUS_USER

    response = requests.get(
        'https://slack.com/api/users.identity',
        params={'token': g.access_token},
    )
    response.raise_for_status()
    users_identity = response.json()

    if not users_identity.get('ok'):
        return ANONYMOUS_USER

    return SlackUser(
        id=users_identity['user']['id'],
        name=users_identity['user']['name'],
        email=users_identity['user']['email'],
    )


def post(slack_code: str) -> Any:
    """Exchange a slack OAuth code for a token and return an encrypted version to the client."""
    response = requests.get(
        'https://slack.com/api/oauth.access',
        auth=HTTPBasicAuth(qdb.CLIENT_ID, qdb.CLIENT_SECRET),
        params={'code': slack_code},
    )
    response.raise_for_status()
    oauth_access = response.json()

    if not oauth_access.get('ok'):
        return abort(403)

    if oauth_access.get('team', {}).get('id') != qdb.SLACK_TEAM_ID:
        return abort(403)

    return Fernet(qdb.SECRET_KEY).encrypt(oauth_access['access_token'].encode())
