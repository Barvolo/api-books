import requests

def get_book_details(isbn):
    try:
        response = requests.get(f"http://books-service:5001/books?ISBN={isbn}")
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException:
        return None