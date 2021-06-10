import enum


class MarkType(enum.Enum):
    X = 'X'
    O = 'O'

    def __str__(self):
        return self.value

    @staticmethod
    def list():
        return [mark.value for mark in MarkType]


class GameResultType(enum.Enum):
    WIN = 'WIN'
    LOSE = 'LOSE'
    DRAW = 'DRAW'

    def __str__(self):
        return self.value

    @staticmethod
    def list():
        return [result.value for result in GameResultType]

