from pymongo import MongoClient
from flask import jsonify, abort, make_response, Response
from datetime import datetime
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
        except:
            msg = 'Connection is failed to DB!'
            return abort(make_response(jsonify(message=msg), 404))

    @staticmethod
    def get_all_user_data(uid):
        """provives all data belong to specific user including guest
        """
        try:
            conn = Database.mongo.germanFlashcards.users
            result = list(conn.find({'userID': uid}, {
                '_id': 0, 'creation_date': 0, 'userID': 0, 'email': 0}))[0]
            if result != []:
                return result
            else:
                raise Exception("No user in DB!")
        except:
            msg = 'User data could not be collected from DB!'
            return abort(make_response(jsonify(message=msg), 404))

    @staticmethod
    def update_user_data(uid, new_topics):
        """Updates all data belong to specific user
        """
        try:
            conn = Database.mongo.germanFlashcards.users
            conn.update({'userID': uid}, {'$set': {'topics': new_topics}})
            return Response(status=200)
        except:
            msg = 'User data could not be updated on DB!'
            return abort(make_response(jsonify(message=msg), 404))

    @staticmethod
    def user_not_exists(uid):
        """Checks if user  existed in DB or not?
        """
        conn = Database.mongo.germanFlashcards.users
        result = list(conn.find({'userID': uid}))
        return True if result == [] else False

    @staticmethod
    def add_new_user(user):
        """Insert new user to users collection
        """
        master_uid = os.environ.get('MASTER')
        now = datetime.now()
        try:
            core_topics = Database.get_all_user_data(master_uid)['topics']
            new_user = {'creation_date': now,
                        'userID': user['userID'],
                        'userName': user['username'],
                        'email': user['email'],
                        'topics': core_topics}

            conn = Database.mongo.germanFlashcards.users
            conn.insert(new_user)
            return Response(status=200)
        except:
            msg = 'User data could not be added to DB!'
            return abort(make_response(jsonify(message=msg), 404))

    @ staticmethod
    def delete_user(user):
        """Delete given user from users collection
        """
        if user['userID'] == os.environ.get('MASTER'):
            msg = "Master user can not be deleted"
            return abort(make_response(jsonify(message=msg), 404))

        try:
            conn = Database.mongo.germanFlashcards.users
            conn.delete_one({'userID': user['userID']})
            return Response(status=200)
        except:
            msg = "User could not be deleted from DB!"
            return abort(make_response(jsonify(message=msg), 404))
