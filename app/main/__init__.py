from flask import Blueprint, render_template, session
from flask_login import login_required

main = Blueprint('main', __name__)


@main.route('/public')
def public_page():
    session['page'] = 'public'
    return render_template('main/public.html')


@main.route('/protected')
@login_required
def private_page():
    session['id'] = '000'
    return render_template('main/protected.html')


@main.route('/session')
def session_page():
    return render_template('main/session.html', session=session)
