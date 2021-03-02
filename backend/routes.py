from flask import Blueprint, request, jsonify
from .db_functions import frontend_user_data, backend_user_data
from backend.db_methods import Database as db
from flask_cors import CORS
import os


api = Blueprint('api', __name__, url_prefix='/api')
cors = CORS(api, resources={
            r'/*': {'origins': 'https://master.d344jh1991oyh.amplifyapp.com'}})


@api.route('/test')
def test():
    """Tests Mongo DB connection
    """
    return f"""<pre>Flask Working correctly</pre>
    <pre>{db.test_connection()}</pre>"""


@api.route('/', methods=['GET'])
def get_all_data():
    """Provides all data belong to the user including guest
    """
    uid = request.headers.get('Authentication')
    # if user is guest or not exist, master user data will be sent
    if (uid == 'guest' or db.user_not_exists(uid)):
        uid = os.environ.get('MASTER')
    result = db.get_all_user_data(uid)
    return jsonify(frontend_user_data(result))


@ api.route('/update-data', methods=['PUT'])
def update_user_flashcards_data():
    """Updates data of given user data on DB
    """
    new_data = request.json
    uid, new_topics = backend_user_data(new_data)
    return db.update_user_data(uid, new_topics)


@ api.route('/add-user', methods=['POST'])
def add_user():
    """Adds new user to the DB
    """
    new_user = request.json
    return db.add_new_user(new_user)


@ api.route('/delete-user', methods=['POST'])
def delete_user():
    """Delete given user from the DB
    """
    user = request.json
    return db.delete_user(user)
