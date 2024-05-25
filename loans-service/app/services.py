import requests
import uuid

def handle_loan_request(data, mongo):
    required_fields = ['memberName', 'ISBN', 'loanDate']
    if not all(field in data for field in required_fields):
        return {"error": "Missing required fields"}, 422

    book_details = get_book_details(data['ISBN'])
    if not book_details:
        return {"error": "Book not found"}, 422
    
    # Check if book is already on loan
    if mongo.db.loans.find_one({"ISBN": data['ISBN'], "returnDate": None}):
        return {"error": "Book is currently on loan"}, 422
    
    # Check if member has reached the loan limit (2 books)
    if mongo.db.loans.count_documents({"memberName": data['memberName'], "returnDate": None}) >= 2:
        return {"error": "Member has reached the loan limit"}, 422
    
    
    
    # Access the first book's details
    book_info = book_details[0]
    data['title'] = book_info.get('title', 'No Title Available')
    data['bookID'] = book_info.get('id', 'No ID Available')

    # Generate a unique loan ID
    data['loanID'] = str(uuid.uuid4())

    # Insert loan data into MongoDB
    mongo.db.loans.insert_one(data)

    # Return the loanID in the response
    return {"loanID": data['loanID']}, 201

    

def get_book_details(isbn):
    try:
        response = requests.get(f"http://books-service:5001/books?ISBN={isbn}")
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException:
        return None
