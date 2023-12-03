from sqlalchemy import func, select

from app import db
from app.games import models as games_models
from app.management import models
from app.management import schemas


class NoLeaguesFoundError(Exception):
    pass


def start_league(league_schema: schemas.LeagueCreate) -> models.League:
    league = models.League(**league_schema.model_dump())

    db.session.add(league)
    db.session.commit()

    return league


def get_rank_table() -> schemas.RankTable:
    last_league_id = (
        db.session.query(models.League.id)
        .filter(
            models.League.started_at
            == db.session.query(func.max(models.League.started_at)).scalar()
        )
        .first()
    )

    if not last_league_id:
        raise NoLeaguesFoundError("No leagues found error")

    last_league_id = last_league_id[0]

    user_total_result_subquery = (
        select(
            [
                games_models.UserGame.user_id,
                func.coalesce(func.sum(games_models.UserGame.game_result), 0).label(
                    "total_result"
                ),
            ]
        )
        .select_from(
            db.join(
                games_models.Game,
                games_models.UserGame,
                games_models.Game.id == games_models.UserGame.game_id,
            )
        )
        .where(games_models.Game.league_id == last_league_id)
        .group_by(games_models.UserGame.user_id)
        .alias("user_total_result")
    )

    main_query = select(
        [
            func.rank()
            .over(order_by=user_total_result_subquery.columns.total_result.desc())
            .label("rank_number"),
            user_total_result_subquery.columns.user_id,
            user_total_result_subquery.columns.total_result,
        ]
    )

    results = db.session.execute(main_query).fetchall()

    schema = schemas.RankTable(
        rank_table=[
            schemas.UserRank(
                rank_number=result.rank_number,
                user_id=result.user_id,
                total_result=result.total_result,
            )
            for result in results
        ]
    )

    return schema
