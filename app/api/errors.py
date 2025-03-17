# Error case use on api calls

from flask import jsonify

def bad_request(msg:str):
    response = jsonify({'error': 'Bad Request', 'message': msg})
    response.status_code = 400
    return response

def not_found(msg:str):
    response = jsonify({'error': 'Not Found', 'message': msg})
    response.status_code = 404
    return response

def no_content(msg:str):
    response = jsonify({'error': 'Not Content', 'message': msg})
    response.status_code = 204
    return response

def unauthorize(msg:str):
    response = jsonify({'error': 'Unauthorize', 'message': msg})
    response.status_code = 401
    return response
    