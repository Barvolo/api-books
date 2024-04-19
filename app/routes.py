from flask import Blueprint, request, jsonify
from .external_apis import fetch_book_details
from urllib.parse import unquote

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
    books[book_id] = {**data, **book_details, "id": str(book_id)}

    # Print to console for debugging (can be removed in production)
    print(f'Book ID {book_id} added:', books[book_id])

    # Return the new book record with status code 201 (Created)
    return jsonify({"id": str(book_id), "status code": str(201)}), 201  # Respond with string ID as per requirement


'''''''''''
@api_blueprint.route('/books', methods=['GET'])
def get_books():
    query_string = request.query_string.decode("utf-8")
    
    if query_string:
        # If query string is present, parse it
        filters = {}
        for query in query_string.split('&'):
            if '%20contains%20' in query:
                field, value = query.split('%20contains%20')
                filters[field.strip()] = value.strip()
            else:
                field, value = query.split('=')
                filters[field.strip()] = value.strip()

        # Filter books based on query
        filtered_books = []
        for book_id, book_data in books.items():
            matches_all_filters = True
            for field, value in filters.items():
                if field in book_data and value not in book_data[field]:
                    matches_all_filters = False
                    break
            if matches_all_filters:
                filtered_books.append(book_data)
        
        return jsonify(filtered_books)
    else:
        # If no query string, return all books
        return jsonify(list(books.values())) , 200

'''''''''''

def find_book_id_by_param(param, value):
    for book_id, book_data in books.items():
        if param in book_data and unquote(value) in book_data[param]:
            return book_id
    return None

@api_blueprint.route('/books', methods=['GET'])
def get_books():
    query_params = request.query_string.decode("utf-8")
    all_books = list(books.values())
    result_books = []  # List to store final filtered books
    seen_book_ids = set()  # Set to keep track of book ids that have already been added
    
    if query_params == '':
        return jsonify(all_books), 200
    for book_id, book_data in books.items():
        result_books.append(book_data)
        for query in query_params.split('&'):
            key, value = query.split('=')
            if key not in book_data or unquote(value) not in book_data[key]:
                result_books.remove(book_data)
                break
        
    return jsonify(result_books), 200

'''''''''''
    for query in query_params.split('&'):
        key, value = query.split('=')
        id = find_book_id_by_param(key, value)
        if id is not None and id not in seen_book_ids:
            seen_book_ids.add(id)
            result_books.append(books[id])
    return jsonify(result_books), 200
'''''''''''
    
@api_blueprint.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    # Attempt to retrieve the book by ID
    book = books.get(book_id)
    if book:
        return jsonify(book), 200
    else:
        return jsonify({"error": "Book not found"}), 404

@api_blueprint.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    # Attempt to retrieve the book by ID
    book = books.get(book_id)
    if book:
        del books[book_id]
        return jsonify({"status": "Book deleted"}), 200
    else:
        return jsonify({"error": "Book not found"}), 404
    
    