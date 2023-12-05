from unittest.mock import patch

from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token

from app.games import schemas as games_schemas
from app.games import views
from tests.conftest import USER_1, USER_2


@patch("app.games.views.create_game")
def test_create_game_response_data_if_success(
    create_game_mock, client: FlaskClient, user, game_schema: games_schemas.GameSchema
):
    create_game_mock.return_value = game_schema
    headers = {"Authorization": f"Bearer {create_access_token(user.id)}"}

    response = client.post(
        "/api/v1/games",
        json={"users": [USER_1, USER_2], "league_id": 1},
        headers=headers,
    )

    assert response.json == {
        "id": 1,
        "league_id": 1,
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
def test_create_game_response_code_if_success(
    create_game_mock, client: FlaskClient, user, game_schema: games_schemas.GameSchema
):
    create_game_mock.return_value = game_schema

    headers = {"Authorization": f"Bearer {create_access_token(user.id)}"}

    response = client.post(
        "/api/v1/games",
        json={"users": [USER_1, USER_2], "league_id": 1},
        headers=headers,
    )

    assert response.status_code == 201


@patch("app.games.views.get_user_games")
def test_get_user_games_response_data_if_success(
    get_user_games_mock,
    client: FlaskClient,
    user,
    games_schema: games_schemas.UserGamesSchema,
):
    get_user_games_mock.return_value = games_schema
    headers = {"Authorization": f"Bearer {create_access_token(user.id)}"}

    response = client.get("/api/v1/games", headers=headers)
    assert response.json == {
        "games": [
            {
                "id": 1,
                "league_id": 1,
                "total_turns": 0,
                "turns_overview": [],
                "created_dttm": "2021-05-31T10:00:00",
                "finished_dttm": None,
                "users": [
                    {"id": 1, "mark": "X", "game_result": None},
                    {"id": 2, "mark": "O", "game_result": None},
                ],
            }
        ]
    }
    assert response.status_code == 200


def test_get_user_games_if_unauthorized(client: FlaskClient):
    response = client.get("/api/v1/games")

    assert response.json == {"message": "Missing Authorization Header"}
    assert response.status_code == 401


def test_get_game_response_if_unauthorized(client: FlaskClient):
    response = client.get("/api/v1/games/999")

    assert response.json == {"message": "Missing Authorization Header"}
    assert response.status_code == 401


@patch("app.games.views.get_game")
@patch("app.games.controllers.get_jwt_identity")
@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request")
def test_get_game_response_data_if_game_not_found(
    _, get_jwt_identity_mock, get_game_mock, user, client: FlaskClient
):
    game_id = 999
    get_jwt_identity_mock.return_value = user.id
    get_game_mock.side_effect = views.GameNotFoundError(f"Game {game_id} not found.")

    response = client.get(f"/api/v1/games/{game_id}")

    assert response.json == {"message": f"Game 999 not found."}


@patch("app.games.views.get_game")
@patch("app.games.controllers.get_jwt_identity")
@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request")
def test_get_game_response_code_if_game_not_found(
    _, get_jwt_identity_mock, get_game_mock, client: FlaskClient, user
):
    game_id = 999
    get_jwt_identity_mock.return_value = user.id
    get_game_mock.side_effect = views.GameNotFoundError(f"Game {game_id} not found.")

    response = client.get(f"/api/v1/games/{game_id}")

    assert response.status_code == 400


@patch("app.games.views.get_game")
@patch("app.games.controllers.get_jwt_identity")
@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request")
def test_get_game_response_data_if_success(
    _,
    get_jwt_identity_mock,
    get_game_mock,
    client: FlaskClient,
    user,
    game_board_schema: games_schemas.GameBoardSchema,
):
    get_game_mock.return_value = game_board_schema
    get_jwt_identity_mock.return_value = user.id

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
@patch("app.games.controllers.get_jwt_identity")
@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request")
def test_get_game_response_code_if_success(
    _,
    get_jwt_identity_mock,
    get_game_mock,
    client: FlaskClient,
    user,
    game_board_schema: games_schemas.GameBoardSchema,
):
    get_game_mock.return_value = game_board_schema
    get_jwt_identity_mock.return_value = user.id

    response = client.get(f"/api/v1/games/{game_board_schema.id}")

    assert response.status_code == 200


@patch("app.games.controllers.get_jwt_identity")
@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request")
def test_patch_game_response_data_if_game_not_found(
    _,
    get_jwt_identity_mock,
    client: FlaskClient,
    user,
    game_board_schema: games_schemas.GameBoardSchema,
):
    game_id = 999
    get_jwt_identity_mock.return_value = user.id
    turn_request_data = game_board_schema.turns_overview[1]

    response = client.patch(f"/api/v1/games/{game_id}", json=dict(turn_request_data))

    assert response.json == {"message": "Game 999 not found."}


@patch("app.games.controllers.get_jwt_identity")
@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request")
def test_patch_game_response_code_if_game_not_found(
    _,
    get_jwt_identity_mock,
    client: FlaskClient,
    user,
    game_board_schema: games_schemas.GameBoardSchema,
):
    game_id = 999
    get_jwt_identity_mock.return_value = user.id
    turn_request_data = game_board_schema.turns_overview[1]

    response = client.patch(f"/api/v1/games/{game_id}", json=dict(turn_request_data))

    assert response.status_code == 400


@patch("app.games.views.make_turn")
@patch("app.games.controllers.get_jwt_identity")
@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request")
def test_patch_game_response_data_if_success(
    _,
    get_jwt_identity_mock,
    make_turn_mock,
    client: FlaskClient,
    user,
    game_board_schema: games_schemas.GameBoardSchema,
):
    get_jwt_identity_mock.return_value = user.id
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
@patch("app.games.controllers.get_jwt_identity")
@patch("flask_jwt_extended.view_decorators.verify_jwt_in_request")
def test_patch_game_response_code_if_success(
    _,
    get_jwt_identity_mock,
    make_turn_mock,
    client: FlaskClient,
    user,
    game_board_schema: games_schemas.GameBoardSchema,
):
    get_jwt_identity_mock.return_value = user.id
    make_turn_mock.return_value = game_board_schema
    user_turn_request = game_board_schema.turns_overview[1]

    response = client.patch(
        f"/api/v1/games/{game_board_schema.id}", json=dict(user_turn_request)
    )

    assert response.status_code == 201
