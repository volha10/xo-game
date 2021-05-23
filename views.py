from enums import MarkType
from models import Game


def create_game(db_connect, user_id):
    game = Game(user_id=user_id, user_mark=MarkType.X.name)
    db_connect.session.add(game)
    db_connect.session.commit()

    return game


def get_game(game_id):
    return None


def make_move(game_id, step_overview):
    return None