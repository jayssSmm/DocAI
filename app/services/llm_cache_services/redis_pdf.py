import hashlib
from app.extensions import redis_client as r

CACHE_TTL = 60 * 60 * 24  # 24 hours

def make_hash_file(file):
    file.seek(0)
    hash_val = hashlib.file_digest(file, 'sha256').hexdigest()
    file.seek(0)
    return hash_val

def set_cache_file(file,response):

    hash_file=make_hash_file(file)

    r.hset('server_history_groq',hash_file,response)

    if r.ttl('server_history_groq') == -1:
        r.expire('server_history_groq',CACHE_TTL)

    return True

def get_cache_file(file):

    hash_file=make_hash_file(file)
    raw = r.hexists('server_history_groq',hash_file)
    if raw:
        return r.hget('server_history_groq',hash_file)
    return None