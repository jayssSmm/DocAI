import redis

r = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

HISTORY_TTL = 60 * 60 * 24  # 24 hours