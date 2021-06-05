import pytest

from app import create_app
from app.games.enums import MarkType
from app.games.models import Game, User


@pytest.fixture
def app():
    """Create and configure new instance for each test."""
    app = create_app('config.TestingConfig')

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def game_x(client):
    user = User(email="user@example.com", name="Test User")
    user.id = 555

    game = Game(user_mark=MarkType.X, user_id=user.id, started_dttm="2021-05-31T10:00:00")
    game.id = 999

    return game
