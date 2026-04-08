from flask import Blueprint

bp = Blueprint('ping',__name__)

@bp.route('/ping')
def ping():
    return 'pong', 200