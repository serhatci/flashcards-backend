from flask import jsonify, Blueprint
from backend.db_connection import Database as db
import re


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/test')
def test():
    return 'Working correctly'


# Provides flash cards titles for home page
@api.route('<string:username>')
def get_titles(username):
    return db.get_titles(username)


# Provides flashcards for user specific titles
@api.route('/<string:username>/<string:title>')
def get_words(username, title):
    return db.get_words(username, title)


# converts titles to camel case for db insert
def camel_case(word):
    snake = ''.join(x.capitalize() for x in word.split(' '))
    return (snake[0].lower() + snake[1:])
