from flask import Blueprint,redirect,render_template
from app.extensions import redis_client as r

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/clear')
def clear():
    r.flushall()
    return redirect('/')