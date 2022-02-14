import os


class BaseConfig:
    SECRET_KEY = 'very-secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    REPO_TYPE = 'MEM'

    GOOGLE_REDIRECT_URI = "http://localhost:5000/oauth/callback/google"
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
    GOOGLE_SCOPE = "openid profile"
    GOOGLE_AUTHORIZE_ENDPOINT = "https://accounts.google.com/o/oauth2/auth"

    KAKAO_REDIRECT_URI = "http://localhost:5000/oauth/callback/kakao"
    KAKAO_CLIENT_ID = os.environ.get('KAKAO_CLIENT_ID')
    KAKAO_CLIENT_SECRET = os.environ.get('KAKAO_CLIENT_SECRET')
    KAKAO_TOKEN_ENDPOINT = "https://kauth.kakao.com/oauth/token"
    KAKAO_SCOPE = "account_email profile_image"
    KAKAO_AUTHORIZE_ENDPOINT = "https://kauth.kakao.com/oauth/authorize"

    def init_app(self, app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True

    def init_app(self, app):
        print('DEV: ')
        for k, v in app.config.items():
            print(k, v)


class ProductionConfig(BaseConfig):
    DEBUG = False

    def init_app(self, app):
        print('PROD: ')


config = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
}
