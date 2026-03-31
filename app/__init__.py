from flask import Flask
from app.routes.main import bp as main_bp
from app.routes.prompt import bp as prompt_bp
from app.routes.uploads import bp as upload_bp
from app.extensions import db 
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = "ss@//42"

    app.register_blueprint(main_bp)
    app.register_blueprint(prompt_bp)
    app.register_blueprint(upload_bp)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_size": 5,
        "max_overflow": 10,
        "pool_timeout": 30,
        "pool_recycle": 1800,
    }

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)


    return app