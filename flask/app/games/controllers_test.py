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
        "message": f"Game 999 not found."
    }


@patch("app.games.views.get_game")
def test_get_game_response_code_if_game_not_found(get_game_mock, client: FlaskClient):
    game_id = 999
    get_game_mock.side_effect = views.GameNotFoundError(f"Game {game_id} not found.")

    response = client.get(f"/api/v1/games/{game_id}")

    assert response.status_code == 400


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


@patch("app.games.views.get_game")
def test_get_game_response_code_if_success(
    get_game_mock,
    client: FlaskClient,
    game_board_schema: games_schemas.GameBoardSchema,
):
    get_game_mock.return_value = game_board_schema

    response = client.get(f"/api/v1/games/{game_board_schema.id}")

    assert response.status_code == 200


def test_patch_game_response_data_if_game_not_found(
    client: FlaskClient,
    game_board_schema: games_schemas.GameBoardSchema,
):
    game_id = 999
    turn_request_data = game_board_schema.turns_overview[1]

    response = client.patch(f"/api/v1/games/{game_id}", json=dict(turn_request_data))

    assert response.json == {
        "message": "Game 999 not found."
    }


def test_patch_game_response_code_if_game_not_found(
    client: FlaskClient,
    game_board_schema: games_schemas.GameBoardSchema,
):
    game_id = 999
    turn_request_data = game_board_schema.turns_overview[1]

    response = client.patch(f"/api/v1/games/{game_id}", json=dict(turn_request_data))

    assert response.status_code == 400


@patch("app.games.views.make_turn")
def test_patch_game_response_data_if_success(
    make_turn_mock,
    client: FlaskClient,
    game_board_schema: games_schemas.GameBoardSchema,
):
    make_turn_mock.return_value = game_board_schema
    turn_request_data = game_board_schema.turns_overview[1]

    response = client.patch(
        f"/api/v1/games/{game_board_schema.id}", json=dict(turn_request_data)
    )

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


@patch("app.games.views.make_turn")
def test_patch_game_response_code_if_success(
    make_turn_mock,
    client: FlaskClient,
    game_board_schema: games_schemas.GameBoardSchema,
):
    make_turn_mock.return_value = game_board_schema
    user_turn_request = game_board_schema.turns_overview[1]

    response = client.patch(
        f"/api/v1/games/{game_board_schema.id}", json=dict(user_turn_request)
    )

    assert response.status_code == 201
