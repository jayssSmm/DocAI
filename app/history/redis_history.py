import redis

r = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

HISTORY_TTL = 60 * 60 * 24  # 24 hours

def set_history(obj,msg_id=None):

    if msg_id is None:
        msg_id=r.incr('counter:default_user')

    r.hset(f'message:{msg_id}',mapping={'role':'assistant','content':obj})
    r.expire(f'message:{msg_id}',HISTORY_TTL)

    r.rpush('chat_history_groq',f'message:{msg_id}')
    r.expire('chat_history_groq', HISTORY_TTL)

    return True
    

def get_last_ten_messages(n:int=10):
    return list(map(lambda x:r.hgetall(x), r.lrange("chat_history_groq",-n,-1)))