from flask import Blueprint, url_for, redirect, request, render_template, current_app
from flask_login import login_user, logout_user

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
