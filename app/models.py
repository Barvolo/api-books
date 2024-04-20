
from flask import request


def is_request_json():
    # Check the Content-Type header first to see if it's 'application/json'
    content_type = request.content_type
    if content_type is None or not content_type.startswith('application/json'):
        return False

    # Try to parse the JSON content
    try:
        request_data = request.get_json()  # This method checks if the mimetype is 'application/json' and parses the JSON
        if request_data is None:
            # If get_json() returned None, it means no JSON body was present
            return False
    except ValueError:
        # If JSON is invalid (ValueError), it's not a valid JSON request
        return False

    # If all checks pass, then it's a valid JSON request
    return True