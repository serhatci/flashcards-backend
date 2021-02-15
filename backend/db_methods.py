from pymongo import MongoClient
from flask import jsonify, abort, make_response, Response
from .db_functions import combine, camel_case


class Database():
    """Includes CRUD methods for MongoDB
    """
    @staticmethod
    def __init__(app) -> object:
        """Creates MongoDB connection of flask app
         """
        Database.mongo = MongoClient(
            app.config['MONGO_URI'], maxPoolSize=50, wtimeout=2500)

    @staticmethod
    def test_connection():
        """Tests Mongo DB connection"""
        return Database.mongo.server_info()

    @staticmethod
    def get_all(uid):
        """provives all data belong to specific user"""
        user_info = Database.get_topics_and_username(uid)
        user_topics = user_info['topics']
        user_flashcards = Database.get_flashcards(user_topics)
        all = combine(user_info, user_flashcards)
        return jsonify(all), 200

    @staticmethod
    def get_topics_and_username(uid):
        """provides all topics and username that belong to user"""
        try:
            conn = Database.mongo.flashcards.users
            topics = list(conn.find(
                {'id': uid}, {'_id': 0, 'topics': 1, 'username': 1}))[0]
            return topics
        except:
            msg = "401: User was not found in DB!"
            abort(make_response(jsonify(message=msg), 401))

    @staticmethod
    def get_flashcards(user_topics):
        """provides all flashcards that belongs to user"""
        try:
            flashcards = {}
            for topic in user_topics:
                title = camel_case(topic['title'])
                words = Database.get_words(title, topic['flashcards'])
                flashcards[title] = words
            return flashcards
        except:
            msg = "404: Flashcards belong to provided user could not be found in DB!"
            abort(make_response(jsonify(message=msg), 404))

    @staticmethod
    def get_words(collection, words_id):
        """provides all words from specific collection"""
        try:
            conn = Database.mongo.flashcards[collection]
            words = list(conn.find(
                {'_id': {'$in': words_id}}, {'_id': 0}))
            return words
        except:
            msg = f"{collection} could not be found in DB"
            abort(make_response(jsonify(message=msg), 404))

    @staticmethod
    def get_master_topics(uid):
        """provides all topics that belong to master user"""
        try:
            conn = Database.mongo.flashcards.users
            topics = list(conn.find(
                {'id': uid}, {'_id': 0, 'topics': 1}))[0]
            return topics
        except:
            msg = "Master user' data could not be collected"
            abort(make_response(jsonify(message=msg), 404))

    @staticmethod
    def add_user(user, master_user):
        """Insert new user to user collection """
        try:
            topics = Database.get_master_topics(master_user)
            user = {**user, **topics}
            conn = Database.mongo.flashcards.users
            conn.insert(user)
            return Response(status=200)
        except:
            msg = "Resource not found"
            abort(make_response(jsonify(message=msg), 404))
