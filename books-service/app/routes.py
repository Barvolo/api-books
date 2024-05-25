import uuid
from flask import Blueprint, request, jsonify, current_app
from app.models import is_request_json
from app.rating import create_rating, delete_rating
from .external_apis import fetch_book_details
from urllib.parse import unquote
from flask_pymongo import PyMongo

api_blueprint = Blueprint('api', __name__)
books = {}

@api_blueprint.route('/books', methods=['POST'])
def create_book():
    # Check if the media type is JSON
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
    
    # Check if the ISBN is already in MongoDB
    existing_book = current_app.mongo.db.books.find_one({"ISBN": data['ISBN']})
    if existing_book:
        return jsonify({"error": "Book with this ISBN already exists"}), 422
    
    
    # Increment book ID here so that it starts from 1
    try:
        # Fetch book details from external sources
        book_details = fetch_book_details(data['ISBN'])
        
        if book_details is None:
            # If no details are found, decrement the book_id and respond with error
            #book_id -= 1
            return jsonify({"error": "no items returned from Google Book API for given ISBN number"}), 400
        # Combine the provided data with fetched details and store in the books dictionary
        data.update(book_details)
        # Insert the book data into MongoDB and get the inserted_id
        data['id'] = str(uuid.uuid4())
        current_app.mongo.db.books.insert_one(data)
        
        #data['id'] = str(inserted_book)  # Using MongoDB's generated ID as 'id'
        # Print to console for debugging (can be removed in production)
        #print(f'Book ID {book_id} added:', books[book_id])

        create_rating(data)
        # Return the new book record with status code 201 (Created)
        return jsonify({"id": data['id'], "status code": str(201)}), 201  # Respond with string ID as per requirement
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_blueprint.route('/books', methods=['GET'])
def get_books():
    SUPPORTED_LANGUAGES = ['heb', 'eng', 'spa', 'chi']
    query_params = request.query_string.decode("utf-8")
    all_books = []
    result_books = []  # List to store final filtered books

    # Fetch all books from MongoDB
    try:
        mongo_books_cursor = current_app.mongo.db.books.find({}, {'_id': 0})
        all_books = list(mongo_books_cursor)
    except Exception as e:
        current_app.logger.error(f"Failed to fetch books from MongoDB: {str(e)}")
        return jsonify({"error": "Failed to fetch books"}), 500
    
    try:
        if query_params == '':
            return jsonify(all_books), 200
        for book_data in all_books:
            result_books.append(book_data)
            for query in query_params.split('&'):
                #if '%20contains%20' in query:
                #    key, value = query.split('%20contains%20')
                #    if key.lower() != 'language' or unquote(value).lower() not in SUPPORTED_LANGUAGES or unquote(value) not in book_data[key]:
                #        result_books.remove(book_data)
                #        break
                #else:
                key, value = query.split('=')
                if key.lower() == 'genre' and value not in ['Fiction', 'Children', 'Biography', 'Science', 'Science Fiction', 'Fantasy','Other']:
                    return jsonify({"error": "Invalid genre"}), 422
                #elif key.lower() == 'language' and (unquote(value).lower() not in SUPPORTED_LANGUAGES or unquote(value).lower() not in book_data[key]):
                #    result_books.remove(book_data)
                #    break
                elif key not in book_data or unquote(value) not in book_data[key] or value == '':
                    result_books.remove(book_data)
                    break
    except:
        return [], 200
        
    return jsonify(result_books), 200
  
@api_blueprint.route('/books/<string:book_id>', methods=['GET'])
def get_book(book_id):
    # Attempt to retrieve the book by ID
    try:
        book = current_app.mongo.db.books.find_one({"id": book_id})
        if book:
            if '_id' in book:
                book['_id'] = str(book['_id'])
            return jsonify(book), 200
        else:
            return jsonify({"error": "Book not found"}), 404
    except:
        return jsonify({"error": "Book not found"}), 404

@api_blueprint.route('/books/<string:book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        # Perform the deletion and check the result
        result = current_app.mongo.db.books.delete_one({"id": book_id})
        if result.deleted_count == 0:
            # If no documents were deleted, return a 404 response
            return jsonify({"error": "Book not found"}), 404
        else:
            # If a document was deleted, proceed to delete related ratings
            delete_rating(book_id)
            return jsonify({"status": "Book deleted"}), 200
    except Exception as e:
        # If there's an exception during the delete operation, log it and return a 500 error
        current_app.logger.error(f"Failed to delete book with ID {book_id}: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500
    
@api_blueprint.route('/books/<string:book_id>', methods=['PUT'])
def update_book(book_id):
    # Check if the media type is JSON
    is_valid, result = is_request_json()
    if not is_valid:
        # Return a 415 status code for all JSON related issues
        return jsonify(result), 415
    
    # Check if the book exists
    book = current_app.mongo.db.books.find_one({"id": book_id})
    if not book:
        return jsonify({"error": "Book not found"}), 404
    
    # Get the update data
    update_data = request.json
    required_fields = ['title', 'authors', 'ISBN', 'genre', 'publisher', 'publishedDate', 'id']

    # Check if all required fields are in the update data
    if not all(field in update_data for field in required_fields):
        return jsonify({"error": "Missing fields, all fields must be provided or invalid argument"}), 422
    
    # Check if length of update data is correct
    if len(update_data) != 7:
        return jsonify({"error": "Too many arguments"}), 422
    
    # Check if the genre is valid
    if update_data['genre'] not in ['Fiction', 'Children', 'Biography', 'Science', 'Science Fiction', 'Fantasy','Other']:
        return jsonify({"error": "Invalid genre"}), 422
    
    # Update the book
    result = current_app.mongo.db.books.update_one({"id": book_id}, {"$set": update_data})
    if result.matched_count == 0:
        return jsonify({"error": "Book not found"}), 404
    if result.modified_count == 0:
        return jsonify({"error": "No updates performed"}), 304  # Not Modified
    return jsonify({"id": book_id}), 200
    

    '''
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
    if len(update_data) != 7:
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
        #'language': update_data['language'],
        #'summary': update_data['summary'],
        'id': book_id  # Preserve the ID
    }
    return jsonify({"id": book_id}), 200

    '''