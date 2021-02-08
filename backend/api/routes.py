from flask import jsonify, Blueprint, request
from backend.db_connection import Database as db
from flask_cors import CORS
import os


api = Blueprint('api', __name__, url_prefix='/api')
CORS(api)


# Tests Mongo DB connection
@api.route('/test')
def test():
    return f'''<pre>Flask Working correctly</pre>
<pre>{db.test_connection()}</pre>'''


# Provides all data belong to the user including guest
@api.route('/', methods=['POST'])
def user_flashcards():
    uid = request.json['uid']
    if uid == "guest":
        uid = os.environ.get('MASTER')
    return db.get_all(uid)
