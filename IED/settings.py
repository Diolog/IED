import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig:
    TODOISM_LOCALES = ['en_US', 'zh_Hans_CN']
    TODOISM_ITEM_PER_PAGE = 20

    BABEL_DEFAULT_LOCALE = TODOISM_LOCALES[0]

    # SERVER_NAME = 'todoism.dev:5000'  # enable subdomain support
    SECRET_KEY = os.getenv('SECRET_KEY', 'a secret string')

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql://root:root@127.0.0.1/IED')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)

class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}