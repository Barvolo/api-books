from typing import Counter
from urllib.parse import unquote
from flask import Blueprint, request, jsonify, current_app


ratings_blueprint = Blueprint('ratings', __name__)

def create_rating(book_id):
    book = current_app.mongo.db.books.find_one({"id": book_id})

    new_rating = {
        'values': [],
        'average': 0.0,
        'title': book['title'],
        'id': book_id
    }
    result = current_app.mongo.db.ratings.insert_one(new_rating)
    if result.inserted_id:
        return jsonify({"status": "Rating initialized for book", "rating_id": str(result.inserted_id)}), 201
    else:
        return jsonify({"error": "Failed to initialize rating"}), 500
    

def delete_rating(rating_id):
    result = current_app.mongo.db.ratings.delete_one({"id": rating_id})
    if result.deleted_count == 0:
        return jsonify({"error": "Rating not found"}), 404
    else:
        return jsonify({"status": "Rating deleted"}), 200
   
        
@ratings_blueprint.route('/ratings', methods=['GET'])
def get_all_ratings():
    
    query_params = request.query_string.decode("utf-8")

    if query_params == '':
        ratings_cursor = current_app.mongo.db.ratings.find({})

    else:
        key, val = query_params.split('=')
        if key != 'id':
            return jsonify({"error": "Invalid query parameter"}), 400
        else:
            ratings_cursor = current_app.mongo.db.ratings.find_one({"id": val})
    
    ratings_cursor = list(ratings_cursor)
    for rating in ratings_cursor:
        if '_id' in rating:
            rating['_id'] = str(rating['_id'])

    if not ratings_cursor:
        return jsonify({"error": "Rating not found"}), 404
    
    return jsonify(ratings_cursor), 200
        
        
   
@ratings_blueprint.route('/ratings/<string:rating_id>', methods=['GET'])
def get_rating(rating_id):
    # Attempt to retrieve the rating by ID
    rating = current_app.mongo.db.ratings.find_one({"id": rating_id})
    if rating:
        if '_id' in rating:
            rating['_id'] = str(rating['_id'])
        return jsonify(rating), 200
    else:
        return jsonify({"error": "Rating not found"}), 404
    

@ratings_blueprint.route('/ratings/<string:book_id>/values', methods=['POST'])
def add_rating_value(book_id):
    # Check if the rating exists
    rating = current_app.mongo.db.ratings.find_one({"id": book_id})
    if not rating:
        return jsonify({"error": "Rating not found"}), 404
    
    data = request.get_json()
    if 'value' not in data or not isinstance(data['value'], int):
        return jsonify({"error": "Invalid data, 'value' must be an integer"}), 400
    # Validate the rating value
    if data['value'] not in {1, 2, 3, 4, 5}:
        return jsonify({"error": "Rating value must be between 1 and 5"}), 422
    
    # Update the existing rating
    new_values = rating['values'] + [data['value']]
    new_average = sum(new_values) / len(new_values)
    current_app.mongo.db.ratings.update_one(
        {"id": book_id},
        {"$set": {"values": new_values, "average": new_average}}
    )
    return jsonify({"new_average": new_average}), 200

    
    
@ratings_blueprint.route('/top', methods=['GET'])
def get_top_books():
    # MongoDB aggregation to filter books with at least 3 ratings and compute averages
    pipeline = [
        {"$match": {"values": {"$exists": True, "$not": {"$size": 0}}}},  # Ensure values array is not empty
        {"$project": {
            "id": 1,
            "title": 1,
            "average": {"$avg": "$values"},  # Calculate the average of values
            "count": {"$size": "$values"}  # Count the number of ratings
        }},
        {"$match": {"count": {"$gte": 3}}}  # Filter books with at least 3 ratings
    ]

    try:
        results = list(current_app.mongo.db.ratings.aggregate(pipeline))
        if not results:
            return jsonify([]), 200  # Return an empty list if no books are eligible

        # Sort results by average score and get top 3 unique scores
        results_sorted = sorted(results, key=lambda x: x['average'], reverse=True)
        top_books = results_sorted[:3]  # Assuming we want the top 3 books

        # Format the results to match expected output
        top_books_formatted = [
            {"id": book["id"], "title": book["title"], "average": round(book["average"], 2)}
            for book in top_books
        ]

        return jsonify(top_books_formatted), 200

    except Exception as e:
        return jsonify({"error": "Failed to fetch top books: " + str(e)}), 500
