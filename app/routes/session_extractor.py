from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models.sessions import Session
from sqlalchemy import select
from flask_jwt_extended import jwt_required, get_jwt_identity

bp=Blueprint('session_extract',__name__)

@bp.route('/session')
@jwt_required()
def get_user_session():
    
    try:
        user_id=get_jwt_identity()

    except Exception as e:
        return jsonify({"error": str(e)}), 401

    sessions = db.session.scalars(select(Session).where(Session.user_id == user_id)).all()

    session_list=[]
    for session in sessions:
        session_list.append({
            'user_id':session.user_id,
            'title':session.title
        })

    return jsonify(session_list)