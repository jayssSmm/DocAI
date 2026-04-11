from flask import Flask
from app.routes.main import bp as main_bp
from app.routes.prompt import bp as prompt_bp
from app.routes.uploads import bp as upload_bp
from app.routes.auth import bp as authorise_bp
from app.routes.session_extractor import bp as session_extractor_bp
from app.routes.ping import bp as ping_bp
from app.routes.logout import bp as logout_bp
from app.extensions import db 
from app.extensions import jwt
from app.models.sessions import Session
from app.models.user import User
from app.models.messages import Message
from flask_migrate import Migrate
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")

    app.register_blueprint(main_bp)
    app.register_blueprint(ping_bp)
    app.register_blueprint(prompt_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(authorise_bp)
    app.register_blueprint(session_extractor_bp)
    app.register_blueprint(logout_bp)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_size": 5,
        "max_overflow": 10,
        "pool_timeout": 30,
        "pool_recycle": 1800,
        "pool_pre_ping": True,
        "connect_args": {"sslmode": "require"},
    }

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config["JWT_COOKIE_SECURE"] = False 
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=5)
    print(app.config["JWT_ACCESS_TOKEN_EXPIRES"])
    app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')

    db.init_app(app)
    jwt.init_app(app)

    migrate = Migrate(app, db)

    return app