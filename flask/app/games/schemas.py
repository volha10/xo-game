from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from app.games.enums import MarkType, GameResultLabel


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


class GameBoardSchema(BaseModel):
    id: int
    total_turns: int
    turns_overview: list = []
    created_dttm: datetime
    finished_dttm: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True


class GameSchema(BaseModel):
    id: int
    total_turns: int
    created_dttm: datetime
    finished_dttm: Optional[datetime] = None
    users: Optional[List[GameUserSchema]] = []

    def model_dump(self, **kwargs):
        data = super(GameSchema, self).model_dump(**kwargs)

        for a in data["users"]:
            a["id"] = a["user"]["id"]
            del a["user"]

        return data

    class Config:
        orm_mode = True
        from_attributes = True
