from datetime import datetime

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship

from app import db


class Game(db.Model):
    __tablename__ = "game"

    id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer, db.ForeignKey("league.id"))
    total_turns = db.Column(db.Integer, default=0)
    turns_overview = db.Column(MutableList.as_mutable(JSONB))
    created_dttm = db.Column(db.DateTime, nullable=False)
    finished_dttm = db.Column(db.DateTime)
    users = relationship("UserGame", back_populates="game")

    def __init__(self, league_id: int):
        self.league_id = league_id
        self.total_turns = 0
        self.turns_overview = []
        self.created_dttm = datetime.utcnow()


class UserGame(db.Model):
    __tablename__ = "user_x_game"

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), primary_key=True)
    game_result = db.Column(db.Integer, nullable=True)
    mark = db.Column(db.String(1), nullable=False)

    user = relationship("User", back_populates="games")
    game = relationship("Game", back_populates="users")

    def __init__(
        self,
        user_id: int,
        game_id: int,
        mark: str,
    ):
        self.user_id = user_id
        self.game_id = game_id
        self.mark = mark
