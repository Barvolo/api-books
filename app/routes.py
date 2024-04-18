from flask import Blueprint, request, jsonify
from .external_apis import fetch_book_details

api_blueprint = Blueprint('api', __name__)
books = {}
book_id = 0

@api_blueprint.route('/books', methods=['POST'])
def create_book():
    global book_id
    data = request.json

    # Validate input data
    if 'ISBN' not in data or 'title' not in data or 'genre' not in data:
        return jsonify({"error": "Missing required book fields: title, ISBN, or genre"}), 400

    # Increment book ID here so that it starts from 1
    book_id += 1
    
    # Fetch book details from external sources
    book_details = fetch_book_details(data['ISBN'])
    if book_details is None:
        # If no details are found, decrement the book_id and respond with error
        book_id -= 1
        return jsonify({"error": "Book details not found for given ISBN"}), 404

    # Combine the provided data with fetched details and store in the books dictionary
    books[book_id] = {**data, **book_details, "id": book_id}

    # Print to console for debugging (can be removed in production)
    print(f'Book ID {book_id} added:', books[book_id])

    # Return the new book record with status code 201 (Created)
    return jsonify({"id": str(book_id), "status code": str(201)}), 201  # Respond with string ID as per requirement

@api_blueprint.route('/books', methods=['GET'])
def get_books():
    # Convert the books dictionary into a list of values
    all_books = list(books.values())
    query_string = request.query_string.decode("utf-8")
    for q in query_string.split('&'):
        key, value = q.split('=')
        all_books = [book for book in all_books if book[key] == value]
        
    # Return the list of books as a JSON array
    return jsonify(all_books), 200

@api_blueprint.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    # Attempt to retrieve the book by ID
    book = books.get(book_id)
    if book:
        return jsonify(book), 200
    else:
        return jsonify({"error": "Book not found"}), 404
