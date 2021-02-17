from flask import Blueprint, request
from backend.db_methods import Database as db
from flask_cors import CORS
import os


api = Blueprint('api', __name__, url_prefix='/api')
cors = CORS(api, resources={r"/*": {"origins": "http://localhost:3000"}})


@api.route('/test')
def test():
    """Tests Mongo DB connection"""
    return f'''<pre>Flask Working correctly</pre>
<pre>{db.test_connection()}</pre>'''


@api.route('/', methods=['GET'])
def user_flashcards():
    """Provides all data belong to the user including guest"""
    uid = request.headers.get('Authentication')
    if uid == "guest":
        uid = os.environ.get('MASTER')
    return db.get_all(uid)


@api.route('/add-user', methods=['POST'])
def add_user():
    """Adds new user to the DB"""
    user_data = request.json
    master_user = os.environ.get('MASTER')
    return db.add_user(user_data, master_user)


@api.route('/delete-user', methods=['POST'])
def delete_user():
    """Delete given user from the DB"""
    user_data = request.json
    return db.delete_user(user_data)
