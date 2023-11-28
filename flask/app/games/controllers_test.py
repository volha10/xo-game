from unittest.mock import patch

from flask.testing import FlaskClient

from app.games import schemas as games_schemas
from app.games import views

from tests.conftest import (
    client,  # noqa
    app,  # noqa
    game_schema,  # noqa
    game_board_schema,  # noqa
    USER_1,
    USER_2,
)


@patch("app.games.views.create_game")
def test_create_new_game_response_data_if_success(
    create_game_mock, client: FlaskClient, game_schema: games_schemas.GameSchema
):
    create_game_mock.return_value = game_schema

    response = client.post(
        "/api/v1/games/",
        json={"users": [USER_1, USER_2]},
    )

    assert response.json == {
        "id": 1,
        "total_turns": 0,
        # "turns_overview": [],
        "created_dttm": "2021-05-31T10:00:00",
        "finished_dttm": None,
        "users": [
            {"id": 1, "mark": "X", "game_result": None},
            {"id": 2, "mark": "O", "game_result": None},
        ],
    }


@patch("app.games.views.create_game")
def test_create_new_game_response_code_if_success(
    create_game_mock, client: FlaskClient, game_schema: games_schemas.GameSchema
):
    create_game_mock.return_value = game_schema

    response = client.post(
        "/api/v1/games/",
        json={"users": [USER_1, USER_2]},
    )

    assert response.status_code == 201


@patch("app.games.views.get_game")
def test_get_game_response_data_if_game_not_found(get_game_mock, client: FlaskClient):
    game_id = 999
    get_game_mock.side_effect = views.GameNotFoundError(f"Game {game_id} not found.")

    response = client.get(f"/api/v1/games/{game_id}")

    assert response.json == {
        "message": f"Game {game_id} not found. "
        f"You have requested this URI [/api/v1/games/{game_id}] "
        "but did you mean /api/v1/games/<int:game_id> or /api/v1/ or /api/v1/docs ?"
    }


@patch("app.games.views.get_game")
def test_get_game_response_code_if_game_not_found(get_game_mock, client: FlaskClient):
    game_id = 999
    get_game_mock.side_effect = views.GameNotFoundError(f"Game {game_id} not found.")

    response = client.get(f"/api/v1/games/{game_id}")

    assert response.status_code == 404


@patch("app.games.views.get_game")
def test_get_game_response_data_if_success(
    get_game_mock,
    client: FlaskClient,
    game_board_schema: games_schemas.GameBoardSchema,
):
    get_game_mock.return_value = game_board_schema

    response = client.get(f"/api/v1/games/{game_board_schema.id}")

    assert response.json == {
        "id": 1,
        "total_turns": 2,
        "turns_overview": [
            {"turn_number": 1, "position": 5, "mark": "X"},
            {"turn_number": 2, "position": 1, "mark": "O"},
        ],
        "created_dttm": "2021-05-31T10:00:00",
        "finished_dttm": None,
    }
    assert response.status_code == 200


@patch("app.games.views.get_game")
def test_get_game_response_code_if_success(
    get_game_mock,
    client: FlaskClient,
    game_board_schema: games_schemas.GameBoardSchema,
):
    get_game_mock.return_value = game_board_schema

    response = client.get(f"/api/v1/games/{game_board_schema.id}")

    assert response.status_code == 200
