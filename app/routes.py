from flask import Blueprint, request, jsonify
from app.models import is_request_json
from app.rating import create_rating, delete_rating
from .external_apis import fetch_book_details
from urllib.parse import unquote

api_blueprint = Blueprint('api', __name__)
books = {}
book_id = 0

@api_blueprint.route('/books', methods=['POST'])
def create_book():
    global book_id
    is_valid, result = is_request_json()
    if not is_valid:
        # Return a 415 status code for all JSON related issues
        return jsonify(result), 415
    
    data = request.json
    # Validate input data
    if 'ISBN' not in data or 'title' not in data or 'genre' not in data or len(data) != 3:
        return jsonify({"error": "Missing required book fields: title, ISBN, or genre or there to many argument"}), 422

    if data['genre'] not in ['Fiction', 'Children', 'Biography', 'Science', 'Science Fiction', 'Fantasy','Other']:
        return jsonify({"error": "Invalid genre"}), 422
    
    # Check if the ISBN is already in the books
    for book in books.values():
        if book['ISBN'] == data['ISBN']:
            return jsonify({"error": "Book with this ISBN already exists"}), 422
    
    # Increment book ID here so that it starts from 1
    try:
        book_id += 1
        
        # Fetch book details from external sources
        book_details = fetch_book_details(data['ISBN'])
        
        if book_details is None:
            # If no details are found, decrement the book_id and respond with error
            book_id -= 1
            return jsonify({"error": "no items returned from Google Book API for given ISBN number"}), 400
        # Combine the provided data with fetched details and store in the books dictionary
        books[book_id] = {**data, **book_details, "id": str(book_id)}

        # Print to console for debugging (can be removed in production)
        print(f'Book ID {book_id} added:', books[book_id])

        create_rating(books[book_id])
        # Return the new book record with status code 201 (Created)
        return jsonify({"id": str(book_id), "status code": str(201)}), 201  # Respond with string ID as per requirement
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_blueprint.route('/books', methods=['GET'])
def get_books():
    SUPPORTED_LANGUAGES = ['heb', 'eng', 'spa', 'chi']
    query_params = request.query_string.decode("utf-8")
    all_books = list(books.values())
    result_books = []  # List to store final filtered books
    try:
        if query_params == '':
            return jsonify(all_books), 200
        for book_id, book_data in books.items():
            result_books.append(book_data)
            for query in query_params.split('&'):
                if '%20contains%20' in query:
                    key, value = query.split('%20contains%20')
                    if key.lower() != 'language' or unquote(value).lower() not in SUPPORTED_LANGUAGES or unquote(value) not in book_data[key]:
                        result_books.remove(book_data)
                        break
                else:
                    key, value = query.split('=')
                    if key.lower() == 'genre' and value not in ['Fiction', 'Children', 'Biography', 'Science', 'Science Fiction', 'Fantasy','Other']:
                        return jsonify({"error": "Invalid genre"}), 422
                    elif key.lower() == 'language' and (unquote(value).lower() not in SUPPORTED_LANGUAGES or unquote(value).lower() not in book_data[key]):
                        result_books.remove(book_data)
                        break
                    elif key not in book_data or unquote(value) not in book_data[key] or value == '':
                        result_books.remove(book_data)
                        break
    except:
        return [], 200
        
    return jsonify(result_books), 200
  
@api_blueprint.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    # Attempt to retrieve the book by ID
    try:
        book = books.get(book_id)
        if book:
            return jsonify(book), 200
        else:
            return jsonify({"error": "Book not found"}), 404
    except:
        return jsonify({"error": "Book not found"}), 404

@api_blueprint.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = books.get(book_id)
    if book:
        del books[book_id]
        delete_rating(book_id)
        return jsonify({"status": "Book deleted"}), 200
    else:
        return jsonify({"error": "Book not found"}), 404

@api_blueprint.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    # Check if the media type is JSON
    is_valid, result = is_request_json()
    if not is_valid:
        # Return a 415 status code for all JSON related issues
        return jsonify(result), 415
    
    # Check if the book exists
    if book_id not in books.keys():
        return jsonify({"error": "Book not found"}), 404
    
    # Get the update data
    update_data = request.json
    required_fields = ['title', 'authors', 'ISBN', 'genre', 'publisher', 'publishedDate', 'language', 'summary', 'id']

    # Check if all required fields are in the update data
    if not all(field in update_data for field in required_fields):
        return jsonify({"error": "Missing fields, all fields must be provided or invalid argument"}), 422
    
    # Check if length of update data is correct
    if len(update_data) != 9:
        return jsonify({"error": "Too many arguments"}), 422
    
    # Check if the genre is valid
    if update_data['genre'] not in ['Fiction', 'Children', 'Biography', 'Science', 'Science Fiction', 'Fantasy','Other']:
        return jsonify({"error": "Invalid genre"}), 422

    # Update the book
    books[book_id] = {
        'title': update_data['title'],
        'authors': update_data['authors'],
        'ISBN': update_data['ISBN'],
        'genre': update_data['genre'],
        'publisher': update_data['publisher'],
        'publishedDate': update_data['publishedDate'],
        'language': update_data['language'],
        'summary': update_data['summary'],
        'id': book_id  # Preserve the ID
    }
    return jsonify({"id": book_id}), 200

