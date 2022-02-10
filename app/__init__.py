from flask import Flask, render_template, Blueprint

from app.extensions import login_manager
from app.main import main
from app.auth import auth as auth_bp
from app.models import User, user_pool


def create_app():
    app = Flask(__name__)
    app.secret_key = 'very-secret'

    init_extensions(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    app.register_blueprint(main, url_prefix="/main")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app


def init_extensions(app):
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        target_user = None
        for user in user_pool:
            if user.get('id') == user_id:
                target_user = user

        if target_user:
            return User(target_user.get('id'), target_user.get('email'), target_user.get('name'),
                        target_user.get('password'))

