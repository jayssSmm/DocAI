import hashlib
import redis

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
CACHE_TTL = 60 * 60 * 24  # 24 hours

def make_hash_file(file):
    return hashlib.file_digest(file, 'sha256').hexdigest()

def set_cache_file(file,response):

    hash_file=make_hash_file(file)

    r.hset('file_history_groq',hash_file,response)
    r.expire('file_history_groq',CACHE_TTL)

    return True

def get_cache_file(file):

    hash_file=make_hash_file(file)
    raw = r.hexists('file_history_groq',hash_file)
    if raw:
        return r.hget('file_history_groq',hash_file)
    return None