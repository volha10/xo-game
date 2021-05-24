import random

from enums import MarkType
from models import Game


def create_game(db_connect, user_id) -> Game:
    user_mark = MarkType.X #TODO: #random.choice([1, 2])

    game = Game(user_id=user_id, user_mark=user_mark)
    db_connect.session.add(game)

    if _is_computer_turns_first(user_mark):
        _turn_computer(game)

    db_connect.session.commit()

    return game


def _is_computer_turns_first(user_mark) -> bool:
    return True if user_mark == MarkType.O else None


def get_game(game_id):
    return Game.query.get_or_404(game_id, description=f"Game {game_id} not found")


def make_turn(db_connect, game_id, turn_overview) -> Game:
    game = Game.query.get_or_404(game_id, description=f"Game {game_id} not found")

    _turn_user(game, turn_overview)
    _turn_computer(game)

    _set_win(game)

    db_connect.session.add(game)
    db_connect.session.commit()

    return game


def _turn_user(game, turn_overview):
    turn_overview["mark"] = game.user_mark

    game.overview = turn_overview
    game.total_turns += 1


def _turn_computer(game: Game):
    step_overview = {
        "turn_number": game.total_turns + 1,
        "position": _generate_position(),
        "mark": MarkType.O if game.user_mark == MarkType.X else MarkType.X
    }

    # Update game overview.
    game.overview = step_overview
    game.total_turns += 1


def _generate_position():
    return 3


def _set_win(game):
    pass
