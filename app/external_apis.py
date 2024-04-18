import requests
import google.generativeai as genai

def fetch_language_from_openlibrary(isbn):
    """Fetch language information from the OpenLibrary API."""
    openlibrary_url = f'https://openlibrary.org/search.json?q=isbn:{isbn}&fields=key,title,author_name,language'
    response = requests.get(openlibrary_url)
    if response.status_code == 200:
        data = response.json()
        if 'docs' in data and data['docs'] and 'language' in data['docs'][0]:
            # Checking the structure of the language field
            language_data = data['docs'][0]['language']
            if isinstance(language_data, list):
                # Assuming language data is a list of languages or language codes
                return language_data
            elif isinstance(language_data, str):
                # If it's a string, return it in a list
                return [language_data]
        else:
            return ["Language not found"]  # Default when no language data is found
    return ["API request failed"] 

def fetch_book_details(isbn):
    """ Fetch book details from Google Books and augment with OpenLibrary language data. """
    test_flag = True  # Set to False to enable GenerativeAI API
    google_books_url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}'
    response = requests.get(google_books_url)
    if response.status_code == 200 and 'items' in response.json() and response.json()['totalItems'] > 0:
        book_info = response.json()['items'][0]['volumeInfo']
        languages = fetch_language_from_openlibrary(isbn)  # Fetch languages from OpenLibrary
        if test_flag:
            summary = 'Summary not available'
        else:
            title = book_info.get("title", "non available")
            promt = f"Summarize the book {title} in 5 sentences or less."
            summary = fetch_summarized_content(promt)
        return {
            "authors": ' and '.join(book_info.get("authors", ["Author not available"])),
            "publisher": book_info.get("publisher", "Publisher not available"),
            "publishedDate": book_info.get("publishedDate", "Date not available"),
            "language": languages,  # Use language data from OpenLibrary
            "summary": summary
        }
    return None


def fetch_summarized_content(text):
    """Fetch summarized content from the GenerativeAI API."""
    genai.configure(api_key="AIzaSyCwwcINB8traD6HMwCX533qhuaowaqBWek")
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(text)
    return response.text
