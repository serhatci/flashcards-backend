from pymongo import MongoClient
from flask import jsonify, abort, make_response, Response
from .db_functions import combine, camel_case
import os


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
                {'userID': uid}, {'_id': 0, 'topics': 1, 'username': 1}))[0]
            return topics
        except:
            msg = "User was not found in DB!"
            abort(make_response(jsonify(message=msg), 401))

    @staticmethod
    def get_flashcards(user_topics):
        """provides all flashcards that belongs to user"""
        # tr
        flashcards = {}
        for topic in user_topics:
            title = camel_case(topic['title'])
            cards = Database.get_words(title, topic['flashcards'])
            flashcards[title] = cards
        return {"flashcards": flashcards}
        # except:
        #     msg = "Flashcards belong to provided user could not be found in DB!"
        #     abort(make_response(jsonify(message=msg), 404))

    @staticmethod
    def get_words(title, card_indexes):
        """provides all words from specific collection"""
        # try:
        conn = Database.mongo.flashcards.flashcards
        all_cards = list(conn.find(
            {'title': title}, {'_id': 0, 'title': 0}))[0]["cards"]
        user_cards = [all_cards[i] for i in card_indexes]
        return user_cards
        # except:
        #     msg = f"{title} could not be found in DB"
        #     abort(make_response(jsonify(message=msg), 404))

    @ staticmethod
    def get_master_topics(uid):
        """provides all topics that belong to master user"""
        try:
            conn = Database.mongo.flashcards.users
            topics = list(conn.find(
                {'id': uid}, {'_id': 0, 'topics': 1}))[0]
            return topics
        except:
            msg = "Master user's data could not be collected"
            abort(make_response(jsonify(message=msg), 404))

    @ staticmethod
    def add_user(user, master_user):
        """Insert new user to users collection"""
        try:
            topics = Database.get_master_topics(master_user)
            user = {**user, **topics}
            conn = Database.mongo.flashcards.users
            conn.insert(user)
            return Response(status=200)
        except:
            msg = "Resource not found"
            abort(make_response(jsonify(message=msg), 404))

    @ staticmethod
    def delete_user(user):
        """Delete given user from users collection"""

        if user['id'] == os.environ.get('MASTER'):
            msg = "Master user can not be deleted"
            abort(make_response(jsonify(message=msg), 404))

        try:
            conn = Database.mongo.flashcards.users
            ans = conn.delete_one(user)
            return Response(status=200)
        except:
            msg = "User can not be deleted from DB"
            abort(make_response(jsonify(message=msg), 404))
