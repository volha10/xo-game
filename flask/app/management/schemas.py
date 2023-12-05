from typing import List

from pydantic import BaseModel


class UserRank(BaseModel):
    rank_number: int
    user_id: int
    total_result: int


class RankTable(BaseModel):
    rank_table: List[UserRank]


class LeagueCreate(BaseModel):
    name: str


class OptionCreate(BaseModel):
    name: str
