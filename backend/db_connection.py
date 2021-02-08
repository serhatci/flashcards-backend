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
    def test_connection():
        """Tests Mongo DB connection"""
        return Database.mongo.server_info()

    @staticmethod
    def get_all(uid):
        user_topics = Database.get_topics(uid)
        user_flashcards = {}
        for topic in user_topics:
            title = Database.camel_case(topic['title'])
            words = Database.get_words(title, topic['flashcards'])
            user_flashcards[title] = words
        all = {"titles":
               [
                   [i["title"],
                    Database.camel_case(i["title"])]
                   for i in user_topics
               ]}
        all = {**all, **user_flashcards}
        return jsonify(all)

    @staticmethod
    def get_topics(uid):
        conn = Database.mongo.flashcards.users
        topics = list(conn.find(
            {'id': uid}, {'_id': 0, 'topics': 1}))[0]['topics']
        return topics

    @staticmethod
    def get_words(collection, words_id):
        conn = Database.mongo.flashcards[collection]
        words = list(conn.find(
            {'_id': {'$in': words_id}}, {'_id': 0}))
        return words

    # converts titels to camel case as collection name
    @staticmethod
    def camel_case(word):
        snake = ''.join(x.capitalize() for x in word.split(' '))
        return (snake[0].lower() + snake[1:])
