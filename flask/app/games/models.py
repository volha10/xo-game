from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableList

from app import db


class Game(db.Model):
    __tablename__ = "game"

    id = db.Column(db.Integer, primary_key=True)
    total_turns = db.Column(db.Integer, default=0)
    overview = db.Column(MutableList.as_mutable(JSONB))
    created_dttm = db.Column(db.DateTime, nullable=False)
    finished_dttm = db.Column(db.DateTime)


class UserGame(db.Model):
    __tablename__ = "user_x_game"

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), primary_key=True)
    game_result = db.Column(db.Integer, nullable=False)
    mark = db.Column(db.Integer, nullable=False)

    user = db.relationship("user", back_populates="games")
    game = db.relationship("game", back_populates="users")
