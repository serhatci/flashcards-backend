import os


class Config(object):
    DEBUG = False
    TESTING = False
    MONGO_URI = os.environ.get('DEV_MONGO_URI')

    SESSION_COOKIE_SECURE = True
    SECRET_KEY = os.environ.get('SECRET_KEY')


class ProductionConfig(Config):
    MONGO_URI = os.environ.get('PROD_MONGO_URI')


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_URI = os.environ.get('DEV_MONGO_URI')

    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    TESTING = True
    MONGO_URI = os.environ.get('DEV_MONGO_URI')

    SESSION_COOKIE_SECURE = False
