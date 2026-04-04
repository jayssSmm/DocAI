from app.extensions import db
from app.models.messages import Message

def add_message(session_id,role,content):
    message =  Message(session_id=session_id,role=role,content=content)
    db.session.add(message)
    db.session.commit()
    return
    