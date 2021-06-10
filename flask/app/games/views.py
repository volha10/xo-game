import random
from datetime import datetime
from typing import Dict, List

from app import db
from app.games.enums import MarkType, GameResultType
from app.games.models import Game

WINNING_COMBINATIONS = [
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9},
    {1, 4, 7},
    {2, 5, 8},
    {3, 6, 9},
    {1, 5, 9},
    {3, 5, 7}
]

BOARD = 3 * 3
WINNING_SEQUENCE = 3


class UpdatingFinishedGameError(Exception):
    pass


class GameNotFoundError(Exception):
    pass


def create_game(user_id: int) -> Game:
    """Create Game object."""
    user_mark = random.choice(MarkType.list())

    game = Game(user_id=user_id, user_mark=user_mark)

    if _is_computer_turns_first(user_mark):
        _turn_computer(game)

    db.session.add(game)
    db.session.commit()

    return game


def _is_computer_turns_first(user_mark: MarkType) -> bool:
    return True if user_mark == MarkType.O.value else False


def get_game(game_id: int, user_id: int) -> Game:
    """Get Game object."""
    game = Game.query.filter_by(id=game_id, user_id=user_id).first()

    if not game:
        raise GameNotFoundError("Game %s not found." % game_id)
    return game


def make_turn(game_id: int, turn_overview: Dict[str, int], user_id: int) -> Game:
    game = Game.query.filter_by(id=game_id, user_id=user_id).first()

    if not game:
        raise GameNotFoundError("Game %s not found." % game_id)
    if game.result:
        raise UpdatingFinishedGameError("Game %s over." % game_id)

    _turn_user(game, turn_overview)

    if not game.result:
        _turn_computer(game)

    db.session.add(game)
    db.session.commit()

    return game


def _turn_user(game: Game, turn_overview: Dict[str, int]) -> None:
    turn_overview["mark"] = game.user_mark.value

    game.overview.append(turn_overview)
    game.total_turns += 1

    _set_game_result(game, mark_to_check=game.user_mark.value)


def _turn_computer(game: Game) -> None:
    computer_mark = MarkType.O.value if game.user_mark == MarkType.X else MarkType.X.value

    game.total_turns += 1
    turn_overview = {
        "turn_number": game.total_turns,
        "position": _generate_position(game.overview),
        "mark": computer_mark
    }

    # Update game overview.
    game.overview.append(turn_overview)

    _set_game_result(game, mark_to_check=computer_mark)


def _generate_position(turns_overview: List[Dict[str, int]]) -> int:
    unavailable_positions = [turn["position"] for turn in turns_overview]

    while True:
        generated_position = random.randint(1, 9)

        if generated_position in unavailable_positions:
            continue
        return generated_position


def _set_game_result(game: Game, mark_to_check: str) -> None:
    turns = [item["position"] for item in game.overview if item["mark"] == mark_to_check]

    if len(turns) < WINNING_SEQUENCE:
        return

    # Check if win/lose.
    for win_combination in WINNING_COMBINATIONS:
        if len(win_combination & set(turns)) == WINNING_SEQUENCE:
            game.result = GameResultType.WIN.value if mark_to_check == game.user_mark.value \
                else GameResultType.LOSE.value
            break
    else:
        # Check if draw.
        if game.total_turns == BOARD:
            game.result = GameResultType.DRAW.value

    if game.result:
        game.finished_dttm = datetime.utcnow()

