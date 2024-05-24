from flask import Blueprint, request, jsonify
from .services import handle_loan_request

loans_bp = Blueprint('loans', __name__)

@loans_bp.route('/loans', methods=['POST'])
def create_loan():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415

    data = request.get_json()
    result, status_code = handle_loan_request(data)
    return jsonify(result), status_code


@loans_bp.route('/loans', methods=['GET'])
def get_loans():
    return jsonify({"loans": []}), 200
