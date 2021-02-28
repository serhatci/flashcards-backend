from pymongo import MongoClient
from flask import jsonify, abort, make_response, Response
from .db_functions import organize_user_data, camel_case, compare_topics
import os


class Database():
    """Includes CRUD methods for MongoDB
    """
    @staticmethod
    def __init__(app) -> object:
        """Creates MongoDB connection of flask app
         """
        try:
            Database.mongo = MongoClient(
                app.config['MONGO_URI'], maxPoolSize=50, wtimeout=2500)
        except Exception as err:
            print(err)

    @staticmethod
    def test_connection():
        """Tests Mongo DB connection
        """
        try:
            return Database.mongo.server_info()
        except Exception as err:
            print(err)

    @staticmethod
    def get_all_user_data(uid):
        """provives all data belong to specific user including guest
        """
        try:
            conn = Database.mongo.germanFlashcards.users
            result = list(conn.find({'userID': uid}, {
                '_id': 0, 'creation_date': 0, 'userID': 0}))[0]
            if result != []:
                return jsonify(organize_user_data(result))
            else:
                raise Exception("no user")
        except:
            msg = 'User data could not be collected from DB!'
            return abort(make_response(jsonify(message=msg), 404))
