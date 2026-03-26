import hashlib
import redis

r = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
CACHE_TTL = 60 * 60 * 24  # 24 hours

def make_hash_file(file):
    file.seek(0)
    hash_val = hashlib.file_digest(file, 'sha256').hexdigest()
    file.seek(0)
    return hash_val

def set_cache_file(file,response):

    hash_file=make_hash_file(file)

    r.hset('cache_history_groq',hash_file,response)

    if r.ttl('cache_history_groq') == -1:
        r.expire('cache_history_groq',CACHE_TTL)

    return True

def get_cache_file(file):

    hash_file=make_hash_file(file)
    raw = r.hexists('cache_history_groq',hash_file)
    if raw:
        return r.hget('cache_history_groq',hash_file)
    return None

# https://youtu.be/s2OccJMWwkM?si=H2Z81j-b_r9NByzP