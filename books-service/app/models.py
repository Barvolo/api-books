
import re
from flask import request


def is_request_json():
    """
    Checks if the incoming request is a valid JSON request.
    This includes checking if the Content-Type is 'application/json' and verifying that the JSON is well-formed.

    Returns:
        tuple: (bool, dict or None) where bool indicates if the request is valid,
               and dict (or None) is the JSON data if valid, or an error message if not valid.
    """
    # Check if the Content-Type is 'application/json'
    if request.headers.get('Content-Type') != 'application/json':
        return False, {"error": "Invalid media type, must be application/json"}

    try:
        # Attempt to parse the JSON data
        data = request.get_json()  # Without force=True, it will return None if not correctly formatted as JSON
        if data is None:
            raise ValueError("Malformed JSON data.")
    except Exception as e:
        # Handle parsing errors or other JSON issues
        return False, {"error": "Invalid JSON data"}

    return True, data


def process_published_date(published_date):
    # Check if the full date "YYYY-MM-DD" is present
    if re.match(r'\d{4}-\d{2}-\d{2}', published_date):
        return published_date  # Date is in the correct format
    # Check if only the year "YYYY" is present
    elif re.match(r'\d{4}', published_date):
        return published_date  # Only the year is present
    else:
        return "missing"  # Neither full date nor year is available









