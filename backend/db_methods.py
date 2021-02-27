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
        """Tests Mongo DB connection
        """
        return Database.mongo.server_info()

    @staticmethod
    def get_all(uid):
        """provives all data belong to specific user
        """
        user_info = Database.get_topics_and_username(uid)
        user_topics = user_info['topics']
        user_flashcards = Database.get_flashcards(user_topics)
        all = combine(user_info, user_flashcards)
        return jsonify(all), 200

    @staticmethod
    def get_topics_and_username(uid):
        """provides all topics and username that belong to user
        """
        conn = Database.mongo.flashcards.users
        topics = list(conn.find(
            {'userID': uid}, {'_id': 0, 'topics': 1, 'username': 1}))[0]
        return topics

    @staticmethod
    def get_flashcards(user_topics):
        """provides all flashcards that belongs to user
        """
        flashcards = {}
        for topic in user_topics:
            title = camel_case(topic['title'])
            cards = Database.get_words(title, topic['flashcards'])
            flashcards[title] = cards
        return {"flashcards": flashcards}

    @staticmethod
    def get_words(title, card_objectID_list):
        """provides all words from specific collection
        """
        try:
            conn = Database.mongo.flashcards.flashcards
            user_cards = list(conn.find(
                {'title': title, 'cards.cardID': {'$in': card_objectID_list}},
                {'_id': 0, 'title': 0,  'cards.cardID': 0}))[0]['cards']
            return user_cards
        except:
            return []

    @ staticmethod
    def get_master_topics(uid):
        """provides all topics that belong to master user
        """
        try:
            conn = Database.mongo.flashcards.users
            topics = list(conn.find(
                {'userID': uid}, {'_id': 0, 'topics': 1}))[0]
            return topics
        except:
            return []

    @ staticmethod
    def add_user(user, master_user):
        """Insert new user to users collection
        """
        topics = Database.get_master_topics(master_user)
        user = {**user, **topics}
        conn = Database.mongo.flashcards.users
        conn.insert(user)
        return Response(status=200)

    @ staticmethod
    def delete_user(user):
        """Delete given user from users collection
        """
        if user['id'] == os.environ.get('MASTER'):
            msg = "Master user can not be deleted"
            abort(make_response(jsonify(message=msg), 404))

        conn = Database.mongo.flashcards.users
        conn.delete_one(user)
        return Response(status=200)

    @ staticmethod
    def update_user_topics(new_data):
        """Update given user topics to new topics
        """
        conn = Database.mongo.flashcards.users
        user_data = Database.get_topics_and_username(new_data['id'])['topics']
        remaining_topics = [
            topic for topic in user_data if topic['title'] in new_data['topics']]
        added_titles = list(set(new_data['topics']) -
                            set([topic['title'] for topic in remaining_topics]))
        new_topics = [{'title': new_topic, 'flashcards': []}
                      for new_topic in added_titles]
        updated_topics = new_topics + remaining_topics
        conn.update({'userID': new_data['id']}, {
                    '$set': {'topics': updated_topics}})
        return Response(status=200)

    @ staticmethod
    def update_user_flashcards(new_data):
        """Update given user topics to new topics"""

        conn = Database.mongo.flashcards.users
        conn.update({"userID": new_data.id}, {"topics": new_data.topics})
        return Response(status=200)
