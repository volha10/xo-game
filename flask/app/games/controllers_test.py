from unittest.mock import patch

from flask.testing import FlaskClient

from app.games import schemas

from tests.conftest import client, app, game_schema, USER_1, USER_2  # noqa


@patch("app.games.views.create_game")
def test_create_new_game_response_data_if_success(
    create_game_mock, client: FlaskClient, game_schema: schemas.GameSchema
):
    create_game_mock.return_value = game_schema

    response = client.post(
        "/api/v1/games/",
        json={"users": [USER_1, USER_2]},
    )

    assert response.json == {
        "id": 1,
        "total_turns": 0,
        "turns_overview": [],
        "created_dttm": "2021-05-31T10:00:00",
        "finished_dttm": None,
        "users": [
            {"id": 1, "mark": "X", "game_result": None},
            {"id": 2, "mark": "O", "game_result": None},
        ],
    }


@patch("app.games.views.create_game")
def test_create_new_game_response_code_if_success(
    create_game_mock, client: FlaskClient, game_schema: schemas.GameSchema
):
    create_game_mock.return_value = game_schema

    response = client.post(
        "/api/v1/games/",
        json={"users": [USER_1, USER_2]},
    )

    assert response.status_code == 201
