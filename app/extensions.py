import os
import redis
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask import jsonify

load_dotenv()

jwt = JWTManager()
db = SQLAlchemy()

database_url = os.getenv("DATABASE_URL")
redis_url = os.getenv("REDIS_URL")

redis_client = redis.Redis.from_url(
    redis_url,
    decode_responses=True
)

@jwt.invalid_token_loader
def invalid_token_callback(error):
    print("Invalid token:", error)
    return jsonify({"error": "Invalid token", "reason": str(error)}), 422

@jwt.unauthorized_loader  
def unauthorized_callback(error):
    print("Unauthorized:", error)
    return jsonify({"error": "Unauthorized", "reason": str(error)}), 401