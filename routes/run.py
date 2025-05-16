from flask import Blueprint, request, jsonify
from services.code_runner import run_code_in_language, get_available_languages

run_bp = Blueprint('run', __name__)

@run_bp.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data.get('code', '')
    stdin = data.get('stdin', '')
    language = data.get('language', 'python')
    result = run_code_in_language(code, stdin, language)
    return jsonify(result)

@run_bp.route('/languages', methods=['GET'])
def languages():
    return jsonify({'languages': get_available_languages()}) 