import requests
from flask import Blueprint, url_for, redirect, request, render_template, current_app, abort
from flask_login import login_user, logout_user
from urllib.parse import urlunsplit, urlencode

from app.proxy import user_repo

auth = Blueprint('auth', __name__)


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
    return request.args.get('code')


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

    print(resp.json())

    return code
