from flask import Blueprint, request, jsonify, current_app
from .services import handle_loan_request

loans_bp = Blueprint('loans', __name__)

@loans_bp.route('/loans', methods=['POST'])
def create_loan():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 415
    data = request.get_json()
    mongo = current_app.mongo
    result, status_code = handle_loan_request(data, mongo)
    return jsonify(result), status_code


'''
@loans_bp.route('/loans', methods=['GET'])
def list_loans():
    result, status_code = get_all_loans(request.app.mongo)
    return jsonify(result), status_code

@loans_bp.route('/loan/<loan_id>', methods=['GET'])
def fetch_loan(loan_id):
    result, status_code = get_loan_by_id(loan_id, request.app.mongo)
    return jsonify(result), status_code

@loans_bp.route('/loan/<loan_id>', methods=['DELETE'])
def delete_loan(loan_id):
    result, status_code = delete_loan_by_id(loan_id, request.app.mongo)
    return jsonify(result), status_code
'''