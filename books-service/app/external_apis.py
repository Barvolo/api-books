import re
from flask import jsonify
import requests
import google.generativeai as genai
from app.models import process_published_date

def fetch_language_from_openlibrary(isbn):
    """Fetch language information from the OpenLibrary API."""
    openlibrary_url = f'https://openlibrary.org/search.json?q=isbn:{isbn}&fields=key,title,author_name,language'
    try:
        response = requests.get(openlibrary_url)
        if response.status_code == 200:
            data = response.json()
            if 'docs' in data and data['docs'] and 'language' in data['docs'][0]:
                # Checking the structure of the language field
                language_data = data['docs'][0]['language']
                if isinstance(language_data, list):
                    return language_data
                elif isinstance(language_data, str):
                    # If it's a string, return it in a list
                    return [language_data]
            else:
                return ["missing"]  # Default when no language data is found
        return ["API request failed"] 
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching language data from OpenLibrary: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error processing language data from OpenLibrary: {e}") from e
    
def fetch_book_details(isbn):
    """ Fetch book details from Google Books and augment with OpenLibrary language data. """
    test_flag = True  # Set to False to enable GenerativeAI API
    google_books_url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}'
    try:
        response = requests.get(google_books_url)
        if response.json()['totalItems'] == 0:
            return None
        book_info = response.json()['items'][0]['volumeInfo']
       
        if response.status_code == 200 and 'items' in response.json() and response.json()['totalItems'] > 0:
            
            #languages = fetch_language_from_openlibrary(isbn)  # Fetch languages from OpenLibrary
            #if test_flag:
            #    summary = 'Summary not available'
            #else:
            #    title = book_info.get("title", "non available")
            #    promt = f"Summarize the book {title} in 5 sentences or less."
            #    summary = fetch_summarized_content(promt)
            #lan = [book_info.get("language", "missing")]
            #if 'en' in lan:
            #    lan = ['eng']

            return {
                "authors": ' and '.join(book_info.get("authors", ["missing"])),
                "publisher": book_info.get("publisher", "missing"),
                "publishedDate": process_published_date(book_info.get("publishedDate", "missing")),
                #"language": languages if languages != ['missing'] else lan ,# Use language data from OpenLibrary
                #"summary": summary
            }
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching book details from Google Books: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Error processing book details: {e}")
    
def fetch_summarized_content(text):
    """Fetch summarized content from the GenerativeAI API."""
    try:
        genai.configure(api_key="")
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(text)
        if not response.text:
            raise ValueError("he GenerativeAI API returned an empty response.")
        return response.text
    except Exception as e:
        raise RuntimeError("unable to connect to GenerativeAI") from e
