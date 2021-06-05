from unittest.mock import patch

from flask.testing import FlaskClient

from app.games.models import Game
from tests.conftest import client, app, game_x  # noqa


@patch("app.games.views.get_game")
def test_get_game(create_game_mock, client: FlaskClient, game_x: Game):
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
    create_game_mock.return_value = game_x

    response = client.get("/api/v1/games/999")

    assert response.json == {
        'id': 999,
        'user_id': 555,
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
    create_game_mock.assert_called_once_with(999)


def test_get_game_if_not_found(client: FlaskClient):
    response = client.get("/api/v1/games/999")

    assert response.json == {
        'message': 'Game 999 not found. '
                   'You have requested this URI [/api/v1/games/999] '
                   'but did you mean /api/v1/games/<int:game_id> or /api/v1/ or /api/v1/docs ?'
    }
    assert response.status_code == 404


@patch("app.games.views.create_game")
def test_create_new_game(create_game_mock, client: FlaskClient, game_x: Game):
    create_game_mock.return_value = game_x
    user_id = 555

    response = client.post("/api/v1/games/", json=dict(user_id=user_id))

    assert response.json == {
        'id': 999,
        'user_id': 555,
        'user_mark': 'X',
        'result': None,
        'total_turns': 0,
        'overview': [],
        'started_dttm': '2021-05-31T10:00:00',
        'finished_dttm': None
    }
    assert response.status_code == 201
    create_game_mock.assert_called_once_with(user_id)


@patch("app.games.views.make_turn")
def test_patch_game(make_turn_mock, client: FlaskClient, game_x: Game):
    game_x.total_turns = 1
    game_x.overview = [
            {
                "turn_number": 1,
                "position": 5,
                "mark": "X"
            }
    ]
    make_turn_mock.return_value = game_x
    game_id = 999
    user_turn_request = {
        "turn_number": 1,
        "position": 5
    }

    response = client.patch(f"/api/v1/games/{game_id}", json=dict(user_turn_request))

    assert response.json == {
        'id': game_id,
        'user_id': 555,
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
    make_turn_mock.assert_called_once_with(game_id, user_turn_request)


def test_patch_game_if_not_found(client: FlaskClient):
    response = client.patch("/api/v1/games/111")

    assert response.json == {
        'message': 'Game 111 not found. '
                   'You have requested this URI [/api/v1/games/111] '
                   'but did you mean /api/v1/games/<int:game_id> or /api/v1/ or /api/v1/docs ?'
    }
    assert response.status_code == 404
