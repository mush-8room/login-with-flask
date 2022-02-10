from flask import Blueprint, url_for, redirect, request, render_template, current_app
from flask_login import login_user, logout_user

from app.models import User, user_pool

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        next = request.args.get('next', '')
        return render_template('auth/login.html', next=next)

    else:
        username = request.form.get('username')
        password = request.form.get('password')
        next = request.form.get('next')
        safe_next_redirect = url_for('index')

        # TODO: make safe
        if next:
            safe_next_redirect = next

        target_user = None
        for user in user_pool:
            if user.get('email') == username and user.get('password') == password:
                target_user = user

        if not target_user:
            return render_template('auth/login.html', error='grant failed')

        user = User(target_user.get('id'), target_user.get('email'), target_user.get('name'),
                    target_user.get('password'))

        login_user(user)

        return redirect(safe_next_redirect)


@auth.route('/logout', methods=['GET', ])
def logout():
    logout_user()
    return redirect(url_for('index'))
