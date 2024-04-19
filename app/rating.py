from urllib.parse import unquote
from flask import Blueprint, request, jsonify

ratings_blueprint = Blueprint('ratings', __name__)
ratings = {}

def create_rating(book):
    ratings[book['id']] = {
            'values': [],  # Start with an empty list of values
            'average': 0.0,  # Initial average is 0.0
            'title': book['title'],  # Title from the book data
            'id': book['id']  # ID from the book data
        }

@ratings_blueprint.route('/ratings', methods=['GET'])
def get_all_ratings():
    # Return all ratings
    query_params = request.query_string.decode("utf-8")
    if query_params == '':
        return jsonify(list(ratings.values())), 200
    try:
        key, val = query_params.split('=')
        if key != 'id':
            return jsonify({"error": "Invalid query parameter"}), 400
        if val not in ratings.keys():
            return jsonify({"error": "Rating not found"}), 404
        return jsonify(ratings[val]), 200
    except ValueError:
        return jsonify({"error": "Invalid query parameter"}), 400
    #return jsonify(list(ratings.values()))

@ratings_blueprint.route('/ratings/<int:rating_id>', methods=['GET'])
def get_rating(rating_id):

    if str(rating_id) in ratings.keys():
        return jsonify(ratings[str(rating_id)]), 200
    else:
        return jsonify({"error": "Rating not found"}), 404