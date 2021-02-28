from pymongo import MongoClient
from flask import jsonify, abort, make_response, Response
from .db_functions import combine, camel_case, compare_topics
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
    def get_all(uid):
        """provives all data belong to specific user
        """
        try:
            user_info = Database.get_topics_and_username(uid)
            existing_topics = user_info['topics']
            user_flashcards = Database.get_flashcards(existing_topics)
            all = combine(user_info, user_flashcards)
            return jsonify(all), 200
        except Exception as err:
            print(err)

    @staticmethod
    def get_topics_and_username(uid):
        """provides all topics and username that belong to user
        """
        try:
            conn = Database.mongo.flashcards.users
            return list(conn.find(
                {'userID': uid}, {'_id': 0, 'topics': 1, 'username': 1}))[0]
        except Exception as err:
            print(err)

    @staticmethod
    def get_flashcards(existing_topics):
        """provides all flashcards that belongs to user
        """
        flashcards = {}
        for topic in existing_topics:
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
                {'_id': 0, 'title': 0, 'owner': 0,  'cards.cardID': 0}))[0]['cards']
            return user_cards
        except:
            return []

    @ staticmethod
    def get_master_topics():
        """provides all topics that belong to master user
        """
        try:
            master_uid = os.environ.get('MASTER')
            conn = Database.mongo.flashcards.users
            topics = list(conn.find(
                {'userID': master_uid}, {'_id': 0, 'topics': 1}))[0]
            return topics
        except:
            return []

    @ staticmethod
    def add_user(user):
        """Insert new user to users collection
        """
        try:
            topics = Database.get_master_topics()
            user = {**user, **topics}
            conn = Database.mongo.flashcards.users
            conn.insert(user)
            return Response(status=200)
        except Exception as err:
            print(err)

    @ staticmethod
    def delete_user(user):
        """Delete given user from users collection
        """
        if user['userID'] == os.environ.get('MASTER'):
            msg = "Master user can not be deleted"
            abort(make_response(jsonify(message=msg), 404))

        try:
            conn = Database.mongo.flashcards.users
            conn.delete_one(user)
            return Response(status=200)
        except Exception as err:
            print(err)

    @ staticmethod
    def update_user_topics(new_data):
        """Update given user topics to new topics
        """
        try:
            uid = new_data['uid']
            existing_topics = Database.get_topics_and_username(uid)['topics']
            updated_topics = compare_topics(
                existing_topics, new_data['topics'])
            Database.update_topics(uid, updated_topics)
            Database.update_flashcards_collection(new_data)
            return Response(status=200)
        except Exception as err:
            print(err)

    @staticmethod
    def update_topics(userID, new_topics):
        """Updates topics of given user
        """
        try:
            conn = Database.mongo.flashcards.users
            conn.update({'userID': userID}, {
                        '$set': {'topics': new_topics}})
        except Exception as err:
            print(err)

    @ staticmethod
    def update_flashcards(title, flashcards):
        """Updates flashcards of given document
        """
        conn = Database.mongo.flashcards.flashcards
        conn.update({'title': title}, {'cards': flashcards})
        return Response(status=200)

    @ staticmethod
    def update_flashcards_collection(new_data):
        """Updates flashcards documents in flashcards collection
        """
        try:
            existing_user_titles = Database.get_user_flashcard_titles(
                new_data['uid'])
            new_user_titles = [camel_case(item) for item in new_data['topics']]
            master_titles = Database.get_master_titles()
            deleted_titles = list(set(existing_user_titles) -
                                  set(new_user_titles)-set(master_titles))
            added_titles = list(
                set(new_user_titles)-set(existing_user_titles)-set(master_titles))
            if added_titles != []:
                Database.add_flashcard_title(
                    new_data['uid'], new_data['userName'], added_titles)
            if deleted_titles != []:
                Database.delete_flashcard_title(deleted_titles)
        except Exception as err:
            print(err)

    @staticmethod
    def get_master_titles():
        """Provides all titles in flashcard collection belong to master user
        """
        conn = Database.mongo.flashcards.flashcards
        try:
            master_titles = list(conn.find(
                {'ownerName': 'master'}, {'_id': 0, 'cards': 0, 'ownerID': 0, 'ownerName': 0}))
        except:
            master_titles = []
        return [item['title'] for item in master_titles]

    @ staticmethod
    def get_user_flashcard_titles(uid):
        """Updates flashcards documents in flashcards collection
        """
        conn = Database.mongo.flashcards.flashcards
        try:
            user_titles = list(conn.find(
                {'ownerID': uid}, {'_id': 0, 'cards': 0, 'ownerID': 0, 'ownerName': 0}))
        except:
            user_titles = []
        return [item['title'] for item in user_titles]

    @ staticmethod
    def add_flashcard_title(uid, username, titles):
        """Adds new flashcards documents in to flashcards collection
        """
        try:
            new_user_titles = [{'ownerID': uid, 'ownerName': username,
                                'title': item, 'cards': [], } for item in titles]
            conn = Database.mongo.flashcards.flashcards
            conn.insert_many(new_user_titles)
        except Exception as err:
            print(err)

    @ staticmethod
    def delete_flashcard_title(titles):
        """Deletes given flashcards documents from flashcards collection
        """
        try:
            conn = Database.mongo.flashcards.flashcards
            conn.delete_many(
                {'title': {'$in': titles}, 'owner': {'$ne': 'master'}})
        except Exception as err:
            print(err)
