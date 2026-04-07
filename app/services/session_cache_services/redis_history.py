from app.extensions import redis_client as r
import json

HISTORY_TTL = 60 * 60 * 24  # 24 hours

def set_history(session_id,role,message):

    key = f'session_id:{session_id}:messages'
    r.rpush(key, json.dumps({'role': role, 'content': message}))
    r.expire(key, HISTORY_TTL)
    return True
    

def get_last_ten_messages(session_id,n:int=10):
    key = f'session_id:{session_id}:messages'
    raw = r.lrange(key, -n, -1)
    return [json.loads(m) for m in raw]