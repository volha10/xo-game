from unittest.mock import patch

from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token

from app.auth.models import User
from app.games.models import Game
from app.games.views import GameNotFoundError
from tests.conftest import client, app, game_x, user  # noqa


@patch("app.games.views.get_game")
def test_get_game(get_game_mock, client: FlaskClient, game_x: Game, user: User):
    game_x.overview = [
            {
                "turn_number": 1,
                "position": 5,
                "mark": "X"
            },
            {
                "turn_number": 2,
                "position": 1,
                "mark": "O"
            }
    ]
    get_game_mock.return_value = game_x
    headers = {
        "Authorization": f"Bearer {create_access_token(user.id)}"
    }

    response = client.get("/api/v1/games/999", headers=headers)

    assert response.json == {
        'id': 999,
        'user_id': user.id,
        'user_mark': 'X',
        'result': None,
        'total_turns': 0,
        'overview': [
            {
                "turn_number": 1,
                "position": 5,
                "mark": "X"
            },
            {
                "turn_number": 2,
                "position": 1,
                "mark": "O"
            }
        ],
        'started_dttm': '2021-05-31T10:00:00',
        'finished_dttm': None
    }
    assert response.status_code == 200
    get_game_mock.assert_called_once_with(999, user.id)


@patch("app.games.views.get_game")
@patch("app.games.controllers.get_jwt_identity")
@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request")
def test_get_game_if_game_not_found(
    _, get_jwt_identity_mock, get_game_mock, client: FlaskClient, user: User
):
    game_id = 999
    get_jwt_identity_mock.return_value = user.id
    get_game_mock.side_effect = GameNotFoundError(f"Game {game_id} not found.")

    response = client.get(f"/api/v1/games/{game_id}")

    assert response.json == {
        "message": f"Game {game_id} not found. "
                   f"You have requested this URI [/api/v1/games/{game_id}] "
                   "but did you mean /api/v1/games/<int:game_id> or /api/v1/ or /api/v1/docs ?"
    }
    assert response.status_code == 404


def test_get_game_if_unauthorized(client: FlaskClient):
    response = client.get("/api/v1/games/999")

    assert response.json == {
        "message": "Missing Authorization Header"
    }
    assert response.status_code == 401




@patch("app.games.views.create_game")
def test_create_new_game(create_game_mock, client: FlaskClient, game_x: Game, user: User):
    create_game_mock.return_value = game_x
    headers = {
        "Authorization": f"Bearer {create_access_token(user.id)}"
    }

    response = client.post("/api/v1/games/", json=dict(user_id=user.id), headers=headers)

    assert response.json == {
        'id': game_x.id,
        'user_id': user.id,
        'user_mark': 'X',
        'result': None,
        'total_turns': 0,
        'overview': [],
        'started_dttm': '2021-05-31T10:00:00',
        'finished_dttm': None
    }
    assert response.status_code == 201
    create_game_mock.assert_called_once_with(user.id)


@patch("app.games.views.make_turn")
def test_patch_game(make_turn_mock, client: FlaskClient, game_x: Game, user):
    game_x.total_turns = 1
    game_x.overview = [
            {
                "turn_number": 1,
                "position": 5,
                "mark": "X"
            }
    ]
    make_turn_mock.return_value = game_x
    user_turn_request = {
        "turn_number": 1,
        "position": 5
    }
    headers = {
        "Authorization": f"Bearer {create_access_token(user.id)}"
    }

    response = client.patch(f"/api/v1/games/{game_x.id}", json=dict(user_turn_request), headers=headers)

    assert response.json == {
        'id': game_x.id,
        'user_id': user.id,
        'user_mark': 'X',
        'result': None,
        'total_turns': 1,
        'overview': [
            {
                "turn_number": 1,
                "position": 5,
                "mark": "X"
            }
        ],
        'started_dttm': '2021-05-31T10:00:00',
        'finished_dttm': None
    }
    assert response.status_code == 201
    make_turn_mock.assert_called_once_with(game_x.id, user_turn_request, user.id)


def test_patch_game_if_not_found(client: FlaskClient, user: User):
    headers = {
        "Authorization": f"Bearer {create_access_token(user.id)}"
    }
    response = client.patch("/api/v1/games/111", headers=headers)

    assert response.json == {
        'message': 'Game 111 not found. '
                   'You have requested this URI [/api/v1/games/111] '
                   'but did you mean /api/v1/games/<int:game_id> or /api/v1/ or /api/v1/docs ?'
    }
    assert response.status_code == 404
