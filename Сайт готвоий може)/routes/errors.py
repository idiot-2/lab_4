from flask import Blueprint, jsonify

errors_bp = Blueprint("errors", __name__)

# 400 Bad Request
@errors_bp.app_errorhandler(400)
def bad_request(e):
    return jsonify({"status": "error", "message": "Bad Request"}), 400

# 404 Not Found
@errors_bp.app_errorhandler(404)
def not_found(e):
    return jsonify({"status": "error", "message": "Not Found"}), 404

# 500 Internal Server Error
@errors_bp.app_errorhandler(500)
def server_error(e):
    return jsonify({"status": "error", "message": "Internal Server Error"}), 500
