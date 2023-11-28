from app import db

from app.auth import models as user_models

from app.games import models as games_models
from app.games import schemas as games_schemas


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


def get_game(game_id: int) -> games_schemas.GameBoardSchema:
    game = games_models.Game.query.filter_by(id=game_id).first()

    if not game:
        raise GameNotFoundError("Game %s not found." % game_id)
    return games_schemas.GameBoardSchema.from_orm(game)
