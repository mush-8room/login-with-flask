import os


class BaseConfig:
    SECRET_KEY = 'very-secret'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    REPO_TYPE = 'MEM'

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
