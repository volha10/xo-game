from datetime import datetime

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableList

from app import db
from app.games.enums import MarkType, GameResultType


class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    user_mark = db.Column(db.Enum(MarkType), nullable=False)
    result = db.Column(db.Enum(GameResultType))
    total_turns = db.Column(db.Integer)
    overview = db.Column(MutableList.as_mutable(JSONB))
    started_dttm = db.Column(db.DateTime, nullable=False)
    finished_dttm = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, user_mark, user_id, result=None, total_turns=0, overview=None, started_dttm=datetime.utcnow()):
        self.user_mark = user_mark
        self.result = result
        self.total_turns = total_turns
        self.overview = overview or []
        self.started_dttm = started_dttm
        self.user_id = user_id

    def __repr__(self):
        return "User %s - Game %s - Result %s" % (self.user_id, self.id, self.result)
