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
    WIN = 2
    LOSS = 0
    DRAW = 1

    def __str__(self):
        return self.name

    @staticmethod
    def list():
        return [result.name for result in GameResultLabel]
