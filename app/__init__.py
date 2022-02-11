import os

from flask import Flask, render_template, Blueprint

from app.config import config
from app.database import db
from app.extensions import login_manager
from app.main import main
from app.auth import auth as auth_bp


def create_app():
    app = Flask(__name__)

    app_config = config.get('dev')()
    app.config.from_object(app_config)
    app_config.init_app(app)

    init_extensions(app)
    init_db(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    app.register_blueprint(main, url_prefix="/main")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app


def init_db(app):
    db.init_app(app)


def init_extensions(app):
    login_manager.init_app(app)
