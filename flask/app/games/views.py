from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel
from app import db

from app.auth.models import User
from app.games.enums import MarkType, GameResultLabel

from app.games.models import Game, UserGame


class UpdatingFinishedGameError(Exception):
    pass


class GameNotFoundError(Exception):
    pass


class NewGameUserSchema(BaseModel):
    id: int
    mark: MarkType


class RelatedUserSchema(BaseModel):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


class GameUserSchema(BaseModel):
    mark: MarkType
    game_result: Optional[GameResultLabel] = None
    user: RelatedUserSchema

    class Config:
        orm_mode = True
        from_attributes = True


class GameSchema(BaseModel):
    id: int
    total_turns: int
    created_dttm: datetime
    finished_dttm: Optional[datetime] = None
    users: List[GameUserSchema]

    def model_dump(self, **kwargs):
        data = super(GameSchema, self).model_dump(**kwargs)

        for a in data["users"]:
            a["id"] = a["user"]["id"]
            del a["user"]

        return data

    class Config:
        orm_mode = True
        from_attributes = True


def create_game(
    player_schema_1: NewGameUserSchema, player_schema_2: NewGameUserSchema
) -> GameSchema:
    """Create Game object."""
    game = Game()
    db.session.add(game)
    db.session.commit()

    user_1 = User.query.filter_by(id=player_schema_1.id).first()
    ug_1 = UserGame(
        user_id=user_1.id, game_id=game.id, mark=player_schema_1.mark.value
    )

    user_2 = User.query.filter_by(id=player_schema_2.id).first()
    ug_2 = UserGame(
        user_id=user_2.id, game_id=game.id, mark=player_schema_2.mark.value
    )

    db.session.add_all([ug_1, ug_2])
    db.session.commit()

    return GameSchema.from_orm(game)
