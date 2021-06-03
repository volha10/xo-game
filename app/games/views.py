import random
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


def create_game(user_id: int) -> Game:
    """Create Game object."""
    user_mark = MarkType.X #TODO: #random.choice([1, 2])

    game = Game(user_id=user_id, user_mark=user_mark)
    db.session.add(game)

    if _is_computer_turns_first(user_mark):
        _turn_computer(game)

    db.session.commit()

    return game


def _is_computer_turns_first(user_mark: MarkType) -> bool:
    return True if user_mark == MarkType.O else None


def get_game(game_id: int) -> Game:
    """Get Game object."""
    return Game.query.get_or_404(game_id, description=f"Game {game_id} not found")


def make_turn(game_id: int, turn_overview: Dict[str, int]) -> Game:
    game = Game.query.get_or_404(game_id, description=f"Game {game_id} not found")

    _turn_user(game, turn_overview)

    if not game.result:
        _turn_computer(game)

    db.session.add(game)
    db.session.commit()

    return game


def _turn_user(game: Game, turn_overview: Dict[str, int]) -> None:
    turn_overview["mark"] = game.user_mark

    game.overview = turn_overview
    game.total_turns += 1

    _check_game_over(game, mark_to_check=game.user_mark)


def _turn_computer(game: Game) -> None:
    computer_mark = MarkType.O if game.user_mark == MarkType.X else MarkType.X

    step_overview = {
        "turn_number": game.total_turns + 1,
        "position": _generate_position(game.overview),
        "mark": computer_mark
    }

    # Update game overview.
    game.overview = step_overview
    game.total_turns += 1

    _check_game_over(game, mark_to_check=computer_mark)


def _generate_position(turns_overview: List[Dict[str, int]]) -> int:
    unavailable_positions = [turn["position"] for turn in turns_overview]

    while True:
        generated_position = random.randint(1, 9)

        if generated_position in [unavailable_positions]:
            continue
        return generated_position


def _check_game_over(game: Game, mark_to_check: MarkType) -> None:
    turns = [item["position"] for item in game.overview if item["mark"] == mark_to_check]

    # Check if win/lose.
    for win_combination in WINNING_COMBINATIONS:
        if len(win_combination & set(turns)) == 3:
            game.result = GameResultType.WIN if mark_to_check == game.user_mark else GameResultType.LOSE
            return

    # Check if draw.
    if game.total_turns == BOARD:
        game.result = GameResultType.DRAW

