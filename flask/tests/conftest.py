import pytest

from app import create_app
from app.auth import schemas as users_schemas
from app.auth.models import User
from app.games import schemas as games_schemas
from app.management import models as management_models
from app.management import schemas as management_schemas

USER_1 = {"id": 1, "mark": "X"}
USER_2 = {"id": 2, "mark": "O"}


@pytest.fixture
def app():
    """Create and configure new instance for each test."""
    app = create_app("app.config.TestingConfig")

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def user():
    user = User(email="user@example.com", name="Test User", password="secret")
    user.id = 555

    return user


@pytest.fixture
def user_schema() -> users_schemas.UserSchema:
    schema = users_schemas.UserSchema(**{"id": 1, "options": [{"option_1": "value_1"}]})
    schema.available_option_list = ["option_1"]
    return schema


@pytest.fixture
def users_schema() -> users_schemas.UsersSchema:
    return users_schemas.UsersSchema(users=[{"id": 1}])


@pytest.fixture
def game_schema() -> games_schemas.GameSchema:
    ru1_schema = games_schemas.RelatedUserSchema.model_validate(USER_1)
    gu1_schema = games_schemas.GameUserSchema(user=ru1_schema, mark=USER_1["mark"])

    ru2_schema = games_schemas.RelatedUserSchema.model_validate(USER_2)
    gu2_schema = games_schemas.GameUserSchema(user=ru2_schema, mark=USER_2["mark"])

    game_schema = games_schemas.GameSchema(
        id=1,
        league_id=1,
        total_turns=0,
        created_dttm="2021-05-31T10:00:00",
        users=[gu1_schema, gu2_schema],
    )

    return game_schema


@pytest.fixture
def games_schema(game_schema) -> games_schemas.UserGamesSchema:
    return games_schemas.UserGamesSchema(games=[game_schema])


@pytest.fixture
def game_board_schema(client) -> games_schemas.GameBoardSchema:
    return games_schemas.GameBoardSchema(
        id=1,
        total_turns=2,
        turns_overview=[
            {"turn_number": 1, "position": 5, "mark": "X"},
            {"turn_number": 2, "position": 1, "mark": "O"},
        ],
        created_dttm="2021-05-31T10:00:00",
    )


@pytest.fixture
def league() -> management_models.League:
    league = management_models.League(
        name="Test League",
        started_at="2021-05-31T10:00:00",
    )
    league.id = 1
    return league


@pytest.fixture()
def league_schema() -> management_schemas.RankTable:
    return management_schemas.RankTable(
        rank_table=[
            {
                "rank_number": 1,
                "user_id": 1,
                "total_result": 100,
            }
        ]
    )
