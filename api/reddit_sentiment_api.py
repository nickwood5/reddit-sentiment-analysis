import imp
from flask import Blueprint, jsonify
import flask
from uuid import uuid4

reddit_sentiment_api = Blueprint('lego_minecraft_api', __name__)

def create_simple_message(type, data):
    return flask.make_response(jsonify({"type": type, "data": data}))

@reddit_sentiment_api.route("/reddit_sentiment/get_id", methods=['GET'])
def get_id():
    id = uuid4()
    return create_simple_message("id", id)