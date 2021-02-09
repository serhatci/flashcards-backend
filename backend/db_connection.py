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
        """provives all data belong to specific user"""
        user_topics = Database.get_topics(uid)
        user_flashcards = Database.get_flashcards(user_topics)
        all = Database.combine(user_topics, user_flashcards)
        return jsonify(all)

    @staticmethod
    def get_topics(uid):
        """provides all topics that belong to user"""
        conn = Database.mongo.flashcards.users
        topics = list(conn.find(
            {'id': uid}, {'_id': 0, 'topics': 1}))[0]['topics']
        return topics

    @staticmethod
    def get_flashcards(user_topics):
        """provides all flashcards from DB that belongs to user"""
        flashcards = {}
        for topic in user_topics:
            title = Database.camel_case(topic['title'])
            words = Database.get_words(title, topic['flashcards'])
            flashcards[title] = words
        return flashcards

    @staticmethod
    def get_words(collection, words_id):
        """provides all words from specific collection"""
        conn = Database.mongo.flashcards[collection]
        words = list(conn.find(
            {'_id': {'$in': words_id}}, {'_id': 0}))
        return words

    @staticmethod
    def combine(user_topics, user_flashcards):
        "combines topics and flashcards to a single dict"
        titles = {"titles":
                  [
                      {"str": i["title"],
                       "camelCase":Database.camel_case(i["title"])}
                      for i in user_topics
                  ]}
        return {**titles, **user_flashcards}

    @staticmethod
    def camel_case(word):
        """converts words or sentences to camelCase"""
        snake = ''.join(x.capitalize() for x in word.split(' '))
        return (snake[0].lower() + snake[1:])
