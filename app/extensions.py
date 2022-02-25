from urllib.parse import urlencode

from flask import url_for, request, redirect
from flask_login import LoginManager

from app.proxy import user_repo

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return user_repo.get(user_id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    query_string = urlencode(request.args)

    return redirect(url_for('auth.login', next=f'{request.path}?{query_string}'))
