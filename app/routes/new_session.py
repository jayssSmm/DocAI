from flask import Blueprint,request
from app.services.llm_services import groq_provider
from app.services.db_services import session_table
from flask_jwt_extended import get_jwt_identity

bp=Blueprint('newsession',__name__)

@bp.route('/session/new')
def get_new_session(prompt):

    user_id = get_jwt_identity()

    session_table.add_session(user_id,(groq_provider.session_title(prompt)))