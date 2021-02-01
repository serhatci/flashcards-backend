from flask import Flask, jsonify, request
from backend.db_connection import Database

from backend.settings import DevelopmentConfig, ProductionConfig, TestingConfig
from backend.api.routes import api


def create_app():
    """Starts flask app
    """
    app = Flask(__name__)

    app.config['JSON_AS_ASCII'] = False  # ads UTF-8 support

    if app.config['ENV'] == 'production':
        app.config.from_object(ProductionConfig)
    elif app.config['ENV'] == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    app.register_blueprint(api)

    Database(app)  # create database connection

    return app
