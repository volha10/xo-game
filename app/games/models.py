from datetime import datetime

from sqlalchemy.dialects.postgresql import JSON, ARRAY

from app import db
from app.games.enums import MarkType, GameResultType


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return "User %s" % self.id


class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    user_mark = db.Column(db.Enum(MarkType), nullable=False)
    result = db.Column(db.Enum(GameResultType))
    total_turns = db.Column(db.Integer, default=0)
    overview = db.Column(ARRAY(JSON))
    started_dttm = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    finished_dttm = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return "User %s - Game %s - Result %s" % (self.user_id, self.id, self.result)
