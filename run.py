from flask import Flask
from backend.db_methods import Database
from backend.settings import DevelopmentConfig, ProductionConfig, TestingConfig
from backend.routes import api

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

Database(app)  # creates database connection


if __name__ == "__main__":
    app.run()
