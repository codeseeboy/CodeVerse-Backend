from flask import Blueprint, jsonify
from services.code_runner import get_available_languages

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint that returns the status of the backend and available languages."""
    try:
        available_languages = get_available_languages()
        return jsonify({
            'status': 'healthy',
            'available_languages': available_languages,
            'message': 'Backend is running and ready to execute code.'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'message': 'Backend is running but encountered an error.'
        }), 500 