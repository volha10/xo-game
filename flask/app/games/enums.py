import enum


class MarkType(enum.Enum):
    X = "X"
    O = "O"

    def __str__(self):
        return self.value

    @staticmethod
    def list():
        return [mark.value for mark in MarkType]


class GameResultLabel(enum.Enum):
    WIN = "WIN"
    LOSE = "LOSS"
    DRAW = "DRAW"
    NONE = "NONE"
