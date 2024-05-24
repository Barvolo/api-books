from flask import Blueprint, request, jsonify

main = Blueprint('main', __name__)

@main.route('/loans', methods=['POST'])
def create_loan():
    return jsonify({"status": "success", "message": "Loan created"}), 201