import enum


class MarkType(enum.Enum):
    X = 1
    O = 2


class GameResultType(enum.Enum):
    WIN = 0
    LOSE = 1
    DRAW = 2
