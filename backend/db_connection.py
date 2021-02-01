from pymongo import MongoClient
from flask import jsonify


class Database():
    """Includes CRUD methods for MongoDB
    """
    @staticmethod
    def __init__(app) -> object:
        """Creates MongoDB connection of flask app

        Args:
            app (obj): Flask object
         """
        Database.mongo = MongoClient(app.config['MONGO_URI'], maxPoolSize=50,
                                     wtimeout=2500)

    @staticmethod
    def get_titles(user):
        conn = Database.mongo.flashcards.users
        words_list = list(conn.find(
            {'userName': user}, {'_id': 0, 'topics': 1}))[0]['topics']
        return jsonify(words_list)

    @staticmethod
    def get_words(user, title):
        conn = Database.mongo.flashcards.users
        words_list = list(conn.find(
            {'userName': user}, {'_id': 0, title: 1}))[0][title]
        conn = Database.mongo.flashcards[title]
        words = list(conn.find(
            {'id': {'$in': words_list}}, {'_id': 0}))
        print(words)
        return jsonify(words)
