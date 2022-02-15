import requests
from flask import Blueprint, url_for, redirect, request, render_template, current_app, abort
from flask_login import login_user, logout_user
from urllib.parse import urlunsplit, urlencode

from app.models import User, Connection
from app.database import db
from app.proxy import user_repo
import base64
import json

auth = Blueprint('auth', __name__)


def parse_id_token(token: str) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        raise Exception("Incorrect id token format")

    payload = parts[1]
    padded = payload + '=' * (4 - len(payload) % 4)
    decoded = base64.b64decode(padded)
    return json.loads(decoded)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        next = request.args.get('next', '')

    else:
        username = request.form.get('username')
        password = request.form.get('password')
        next = request.form.get('next')
        safe_next_redirect = url_for('index')

        # TODO: make safe
        if next:
            safe_next_redirect = next

        user = user_repo.get_by_username(username)
        if user.password == password:
            login_user(user)
            return redirect(safe_next_redirect)

    return render_template('auth/login.html', next=next)


@auth.route('/logout', methods=['GET', ])
def logout():
    logout_user()
    return redirect(url_for('index'))


@auth.route('/login/authorize/<target>', methods=['GET', ])
def authorize(target):
    if target not in ['google', 'kakao']:
        return abort(404)

    target = str.upper(target)

    authorize_endpoint = current_app.config.get(f'{target}_AUTHORIZE_ENDPOINT')
    client_id = current_app.config.get(f'{target}_CLIENT_ID')
    redirect_uri = current_app.config.get(f'{target}_REDIRECT_URI')
    response_type = 'code'
    scope = current_app.config.get(f'{target}_SCOPE')

    query_string = urlencode(dict(
        redirect_uri=redirect_uri,
        scope=scope,
        client_id=client_id,
        response_type=response_type
    ))

    authorize_redirect = f'{authorize_endpoint}?{query_string}'

    return redirect(authorize_redirect)


@auth.route('/oauth/callback/kakao', methods=['GET', ])
def kakao_callback():
    code = request.args.get('code')
    token_endpoint = current_app.config.get('KAKAO_TOKEN_ENDPOINT')
    client_id = current_app.config.get('KAKAO_CLIENT_ID')
    client_secret = current_app.config.get('KAKAO_CLIENT_SECRET')
    redirect_uri = current_app.config.get('KAKAO_REDIRECT_URI')
    grant_type = 'authorization_code'

    resp = requests.post(token_endpoint, data=dict(
        code=code,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        grant_type=grant_type,
    ))

    access_token = resp.json().get('access_token')

    profile_resp = requests.get('https://kapi.kakao.com/v2/user/me', headers=dict(
        authorization=f'Bearer {access_token}'
    ))

    import pprint
    pp = pprint.PrettyPrinter()
    pp.pprint(profile_resp.json())

    email = profile_resp.json()['kakao_account']['email']
    user = db.session.query(User).filter(
        User.email == email
    ).first()
    if user:
        login_user(user.to_entity())
    else:
        user = User(
            name='',
            email=email,
            password='',
        )
        db.session.add(user)
        db.session.commit()
        login_user(user.to_entity())

    connection = Connection()
    connection.provider_id = 'kakao'
    connection.profile_url = profile_resp.json()['properties']['profile_image']
    connection.user = user
    connection.access_token = resp.json().get('access_token')
    db.session.add(connection)
    db.session.commit()

    return redirect(url_for('index'))

    # return 'hello'


@auth.route('/oauth/callback/google', methods=['GET', ])
def google_callback():
    code = request.args.get('code')
    token_endpoint = current_app.config.get('GOOGLE_TOKEN_ENDPOINT')
    client_id = current_app.config.get('GOOGLE_CLIENT_ID')
    client_secret = current_app.config.get('GOOGLE_CLIENT_SECRET')
    redirect_uri = current_app.config.get('GOOGLE_REDIRECT_URI')
    grant_type = 'authorization_code'

    resp = requests.post(token_endpoint, data=dict(
        code=code,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        grant_type=grant_type,
    ))

    # import jwt
    #
    # d = jwt.decode(resp.json()['id_token'], algorithms="RS256")
    # print(d)

    d = parse_id_token(resp.json()['id_token'])
    # print(d)
    import pprint
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(d)

    email = d['email']
    user = db.session.query(User).filter(
        User.email == email
    ).first()
    if user:
        login_user(user.to_entity())
    else:
        user = User(
            name='',
            email=email,
            password='',
        )
        db.session.add(user)
        db.session.commit()
        login_user(user.to_entity())

    connection = Connection()
    connection.provider_id = 'google'
    connection.user = user
    connection.access_token = resp.json().get('access_token')
    db.session.add(connection)
    db.session.commit()

    return redirect(url_for('index'))

# kapi.kakao.com//v2/user/me
