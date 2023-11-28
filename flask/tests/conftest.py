import pytest

from app import create_app
from app.auth.models import User
from app.games import schemas as games_schemas

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
def user(client):
    user = User(email="user@example.com", name="Test User", password="secret")
    user.id = 555

    return user


@pytest.fixture
def game_schema(client) -> games_schemas.GameSchema:

    ru1_schema = games_schemas.RelatedUserSchema.model_validate(USER_1)
    gu1_schema = games_schemas.GameUserSchema(user=ru1_schema, mark=USER_1["mark"])

    ru2_schema = games_schemas.RelatedUserSchema.model_validate(USER_2)
    gu2_schema = games_schemas.GameUserSchema(user=ru2_schema, mark=USER_2["mark"])

    game_schema = games_schemas.GameSchema(
        id=1,
        total_turns=0,
        created_dttm="2021-05-31T10:00:00",
        users=[gu1_schema, gu2_schema],
    )

    return game_schema


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
