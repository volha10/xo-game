from datetime import datetime
from typing import List
from typing import Optional

from pydantic import BaseModel

from app.games.enums import MarkType, GameResultLabel


class Turn(BaseModel):
    turn_number: int
    mark: str
    position: int


class GameCreateSchema(BaseModel):
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


class GameBoardSchema(BaseModel):
    id: int
    total_turns: int
    turns_overview: List[Turn] = []
    created_dttm: datetime
    finished_dttm: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True


class GameSchema(BaseModel):
    id: int
    league_id: int
    total_turns: int
    turns_overview: List[Turn] = []
    created_dttm: datetime
    finished_dttm: Optional[datetime] = None
    users: Optional[List[GameUserSchema]] = []

    def model_dump(self, **kwargs):
        data = super(GameSchema, self).model_dump(**kwargs)

        for item in data["users"]:
            item["id"] = item["user"]["id"]
            del item["user"]

        return data

    class Config:
        orm_mode = True
        from_attributes = True


class UserGamesSchema(BaseModel):
    games: List[GameSchema] = []

    def model_dump(self, **kwargs):
        data = super(UserGamesSchema, self).model_dump(**kwargs)

        for game in data["games"]:
            for user in game["users"]:
                user["id"] = user["user"]["id"]
                del user["user"]

        return data

    class Config:
        orm_mode = True
        from_attributes = True
