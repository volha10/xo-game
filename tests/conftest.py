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
    user = User(id=555, email="user@example.com", name="Test User")
    game = Game(id=999, user_mark=MarkType.X, user_id=user.id)

    return game
