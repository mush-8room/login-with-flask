from flask import Flask, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app.api import api as api_bp
from app.auth import auth as auth_bp
from app.config import config
from app.database import db, migrate
from app.extensions import login_manager
from app.main import main
from app.models import User, Connection, Token, Client, AuthorizationCode
from app.oauth import oauth as oauth_bp
from app.oauth.grants import RefreshTokenGrant, AuthorizationCodeGrant, PasswordGrant
from app.oauth.server import oauth_server, query_client, save_token, require_oauth, init_oauth


def create_app(config_name='dev'):
    app = Flask(__name__)

    app_config = config.get(config_name)()
    app.config.from_object(app_config)
    app_config.init_app(app)

    init_extensions(app)
    init_db(app)
    init_oauth(app, db.session)

    if app.debug:
        init_admin(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    app.register_blueprint(main, url_prefix="/main")
    app.register_blueprint(auth_bp, )
    app.register_blueprint(oauth_bp, url_prefix="/oauth")
    app.register_blueprint(api_bp, url_prefix="/api")

    return app


def init_db(app):
    db.init_app(app)
    migrate.init_app(app, db)


def init_extensions(app):
    login_manager.init_app(app)


def init_admin(app):
    admin = Admin(app, name='Login With Flask', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Connection, db.session))
    admin.add_view(ModelView(Client, db.session))
    admin.add_view(ModelView(Token, db.session))
    admin.add_view(ModelView(AuthorizationCode, db.session))
