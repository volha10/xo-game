from datetime import datetime
from app import db

from app.auth import models as user_models

from app.games import models as games_models
from app.games import schemas as games_schemas
from app.games import enums


WINNING_COMBINATIONS = [
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9},
    {1, 4, 7},
    {2, 5, 8},
    {3, 6, 9},
    {1, 5, 9},
    {3, 5, 7},
]

BOARD = 3 * 3
WINNING_SEQUENCE = 3


class UpdatingFinishedGameError(Exception):
    pass


class GameNotFoundError(Exception):
    pass


def create_game(
    player_schema_1: games_schemas.NewGameUserSchema,
    player_schema_2: games_schemas.NewGameUserSchema,
) -> games_schemas.GameSchema:
    game = games_models.Game()
    db.session.add(game)
    db.session.commit()

    user_1 = user_models.User.query.filter_by(id=player_schema_1.id).first()
    ug_1 = games_models.UserGame(
        user_id=user_1.id, game_id=game.id, mark=player_schema_1.mark.value
    )

    user_2 = user_models.User.query.filter_by(id=player_schema_2.id).first()
    ug_2 = games_models.UserGame(
        user_id=user_2.id, game_id=game.id, mark=player_schema_2.mark.value
    )

    db.session.add_all([ug_1, ug_2])
    db.session.commit()

    return games_schemas.GameSchema.from_orm(game)


def get_game(game_id: int, user_id: int) -> games_schemas.GameBoardSchema:
    user_game = games_models.UserGame.query.filter_by(
        game_id=game_id, user_id=user_id
    ).first()

    if not user_game:
        raise GameNotFoundError("Game %s not found." % game_id)
    return games_schemas.GameBoardSchema.from_orm(user_game.game)


def make_turn(
    game_id: int, turn_user_id: id, turn: games_schemas.Turn
) -> games_schemas.GameBoardSchema:
    game = games_models.UserGame.query.filter_by(
        game_id=game_id, user_id=turn_user_id
    ).first()

    if not game:
        raise GameNotFoundError("Game %s not found." % game_id)
    if game.finished_dttm:
        raise UpdatingFinishedGameError("Game %s is over." % game_id)

    _turn_user(game, turn)
    _set_game_result(game, turn_mark=turn.mark)

    db.session.add(game)
    db.session.commit()

    return games_schemas.GameBoardSchema.from_orm(game)


def _turn_user(game: games_models.Game, turn: games_schemas.Turn) -> None:
    game.turns_overview.append(turn.model_dump())
    game.total_turns += 1


def _set_game_result(game: games_models.Game, turn_mark: str) -> None:
    turns_history = [
        item["position"] for item in game.turns_overview if item["mark"] == turn_mark
    ]

    if len(turns_history) < WINNING_SEQUENCE:
        return

    # Check if win/lose.
    for win_combination in WINNING_COMBINATIONS:
        if len(win_combination & set(turns_history)) == WINNING_SEQUENCE:

            for user in game.users:
                if user.mark == turn_mark:
                    user.game_result = enums.GameResultLabel.WIN.value
                else:
                    user.game_result = enums.GameResultLabel.LOSS.value

            game.finished_dttm = datetime.utcnow()
            break
    else:
        # Check if draw.
        if game.total_turns == BOARD:
            for user in game.users:
                user.game_result = enums.GameResultLabel.DRAW.value

            game.finished_dttm = datetime.utcnow()
