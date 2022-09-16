from flask import Blueprint, jsonify
import flask, reddit_api_test, requests
from uuid import uuid4

reddit_sentiment_api = Blueprint('reddit_sentiment_api', __name__)

def create_simple_message(type, data):
    return flask.make_response(jsonify({"type": type, "data": data}))

@reddit_sentiment_api.route("/reddit_sentiment/get_id", methods=['GET'])
def get_id():
    id = uuid4()
    return create_simple_message("id", id)

@reddit_sentiment_api.route("/reddit_sentiment/is_subreddit_valid/<string:subreddit>", methods=['GET'])
def is_subreddit_valid(subreddit: str):
    if reddit_api_test.is_subreddit_valid(subreddit):
        return create_simple_message("valid_subreddit", True)
    else:
        return create_simple_message("valid_subreddit", False)