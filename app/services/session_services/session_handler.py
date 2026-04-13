from app.services.message_services import message_add
from app.services.session_cache_services import redis_history
from app.services.llm_cache_services import redis_text

def get_redis_history(session_id,is_guest,data):
    chat_history=redis_history.get_last_ten_messages(session_id)

    if not chat_history and not is_guest:
        session_history = message_add.get_message(session_id)
        for data in session_history:
                redis_history.set_history(session_id,data['role'],data['content'])
        chat_history = redis_history.get_last_ten_messages(session_id)
    
    return chat_history

def set_redis_history(prompt,response,session_id):
    redis_text.set_cached_response(prompt,response) 

    redis_history.set_history(session_id,'user',prompt)
    redis_history.set_history(session_id,'assistant',response)