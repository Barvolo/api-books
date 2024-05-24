from typing import Counter
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

def delete_rating(rating_id):
    try:
        del ratings[str(rating_id)]
    except KeyError:
        pass
        
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
   
@ratings_blueprint.route('/ratings/<int:rating_id>', methods=['GET'])
def get_rating(rating_id):
    # Attempt to retrieve the rating by ID
    if str(rating_id) in ratings.keys():
        return jsonify(ratings[str(rating_id)]), 200
    else:
        return jsonify({"error": "Rating not found"}), 404
    
@ratings_blueprint.route('/ratings/<int:book_id>/values', methods=['POST'])
def add_rating_value(book_id):
    book_id = str(book_id)  # Convert to string for dictionary key
    # Attempt to retrieve the rating by ID
    if book_id in ratings.keys():
        # Get the rating value from the request
        data = request.get_json()
        if 'value' not in data or not isinstance(data['value'], int):
            return jsonify({"error": "Invalid data, 'value' must be an integer"}), 400
        # Validate the rating value
        if data['value'] not in {1, 2, 3, 4, 5}:
            return jsonify({"error": "Rating value must be between 1 and 5"}), 422

        # Add the new rating value to the list of values
        ratings[book_id]['values'].append(data['value'])

        # Calculate the new average rating
        total = sum(ratings[book_id]['values'])
        count = len(ratings[book_id]['values'])
        new_average = round(total / count, 2)  # Round to 2 decimal places

        # Update the average in the ratings dictionary
        ratings[book_id]['average'] = new_average

        # Return the new average rating
        return jsonify({"new_average": new_average}), 200
    else:
        return jsonify({"error": "Rating not found"}), 404
    
@ratings_blueprint.route('/top', methods=['GET'])
def get_top_books():
    # Filter books that have at least 3 ratings
    eligible_books = {book_id: data for book_id, data in ratings.items() if len(data['values']) >= 3}

    # Compute the top three scores
    if not eligible_books:
        return jsonify([]), 200  # Return an empty list if no books are eligible

    # Gather all eligible scores
    scores = [data['average'] for data in eligible_books.values()]

    # Use a Counter to count frequencies of each score
    score_frequencies = Counter(scores)

    # Sort the scores and extract the top 3 unique scores
    top_three_scores = sorted(score_frequencies.keys(), reverse=True)[:3]

    # Build the dictionary for the top 3 scores with their frequencies
    top_scores_dict = {score: score_frequencies[score] for score in top_three_scores}

    cumulative_count = 0
    top_books = []
    for score, count in top_scores_dict.items():
        cumulative_count += count
        top_books.extend([
            {
                'id': book_id,
                'title': data['title'],
                'average': data['average']
            }
            for book_id, data in eligible_books.items() if data['average'] == score
        ])
        if cumulative_count >= 3:
            break

    top_books_sorted = sorted(top_books, key=lambda x: x['average'], reverse=True)
    return jsonify(top_books_sorted), 200

