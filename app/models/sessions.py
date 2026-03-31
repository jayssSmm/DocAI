from app.extensions import db

class Session(db.model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, )