from app.extensions import db
from app.models.messages import Message
from app.services.cache_services import redis_text

def add_message(session_id,role,content):
    is_statefull = redis_text.is_stateful(content)
    message =  Message(session_id=session_id,role=role,content=content,is_statefull=is_statefull)
    db.session.add(message)
    db.session.commit()
    return
    