from flask import Blueprint, request,jsonify,redirect,url_for,session

routes_api = Blueprint('routes_api', __name__)



@routes_api.route('/api/prueba')
def prueba():
    return jsonify({'success': 'ok'})
