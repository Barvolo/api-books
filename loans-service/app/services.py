import requests
import uuid
from .models import get_book_details

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

def get_all_loans(mongo, query_params):
    # Ensure only valid fields are included and log them
    valid_fields = ['memberName', 'ISBN', 'title', 'bookID', 'loanDate', 'loanID']
    formatted_query_params = {key: query_params[key] for key in query_params if key in valid_fields}
    
    loans = mongo.db.loans.find(formatted_query_params)
    loans = list(loans)
    for loan in loans:
        loan['_id'] = str(loan['_id'])
    return loans, 200
    

def get_loan_by_id(loan_id, mongo):
    loan = mongo.db.loans.find_one({"loanID": loan_id})
    if not loan:
        return {"error": "Loan not found"}, 404
    loan['_id'] = str(loan['_id'])
    return loan, 200

def delete_loan_by_id(loan_id, mongo):
    result = mongo.db.loans.delete_one({"loanID": loan_id})
    if result.deleted_count == 0:
        return {"error": "Loan not found"}, 404
    return {"message": f"Loan {loan_id} deleted successfully"}, 200