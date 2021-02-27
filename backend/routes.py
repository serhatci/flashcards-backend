from flask import Blueprint, request, abort, make_response, jsonify
from backend.db_methods import Database as db
from flask_cors import CORS
import os


api = Blueprint('api', __name__, url_prefix='/api')
cors = CORS(api, resources={r"/*": {"origins": "http://localhost:3000"}})


@api.route('/test')
def test():
    """Tests Mongo DB connection
    """
    try:
        return f'''<pre>Flask Working correctly</pre>
                <pre>{db.test_connection()}</pre>'''
    except:
        msg = "Error occurred in DB connection!"
        abort(make_response(jsonify(message=msg), 404))


@api.route('/', methods=['GET'])
def get_flashcards():
    """Provides all data belong to the user including guest
    """
    try:
        uid = request.headers.get('Authentication')
        if uid == "guest":
            uid = os.environ.get('MASTER')
        return db.get_all(uid)
    except:
        msg = "Data could not be collected from DB!"
        abort(make_response(jsonify(message=msg), 404))


@api.route('/update-data', methods=['PUT'])
def update_user_flashcards_data():
    """Updates given user data to new flashcards data
    """
    try:
        new_data = request.json
        if (new_data["topics"] or new_data["topics"] == []):
            return db.update_user_topics(new_data)
        return db.update_user_flashcards(new_data)
    except:
        msg = "User data could not be updated!"
        abort(make_response(jsonify(message=msg), 404))


@api.route('/add-user', methods=['POST'])
def add_user():
    """Adds new user to the DB
    """
    try:
        user_data = request.json
        master_user = os.environ.get('MASTER')
        return db.add_user(user_data, master_user)
    except:
        msg = "User could not be added to DB!"
        abort(make_response(jsonify(message=msg), 404))


@api.route('/delete-user', methods=['POST'])
def delete_user():
    """Delete given user from the DB
    """
    try:
        user_data = request.json
        return db.delete_user(user_data)
    except:
        msg = "User could not be deleted from DB!"
        abort(make_response(jsonify(message=msg), 404))
