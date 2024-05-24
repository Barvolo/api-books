import requests

def handle_loan_request(data):
    required_fields = ['memberName', 'ISBN', 'loanDate']
    if not all(field in data for field in required_fields):
        return {"error": "Missing required fields"}, 422

    book_details = get_book_details(data['ISBN'])
    if not book_details:
        return {"error": "Book not found"}, 422
    
    # Simulated check if book is on loan
    if False:
        return {"error": "Book is on loan"}, 422
    
    # Simulated check if member can loan more books
    if False:
        return {"error": "Member cannot loan more books"}, 422
    

    # Simulated loan ID creation logic
    loan_id = "LN" + data['ISBN'][-4:]  # Simplistic loan ID creation based on ISBN
    return {"loanID": loan_id}, 201

def get_book_details(isbn):
    try:
        response = requests.get(f"http://localhost:5001/books?ISBN={isbn}")
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException:
        return None
