from flask_jwt_extended import unset_jwt_cookies
from flask import Blueprint,jsonify,redirect

bp=Blueprint("logout",__name__)

@bp.route('/logout', methods=['POST','GET'])
def logout():
    response = jsonify({'message': 'Logged out'})
    unset_jwt_cookies(response)  
    return redirect('/')