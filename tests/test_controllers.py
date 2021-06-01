from unittest.mock import patch


@patch("app.games.views.get_game")
def test_get_game(create_game_mock, client, game_x):
    create_game_mock.return_value = game_x

    response = client.get("/api/v1/games/999")

    assert response.json == {
        'id': 999,
        'user_id': 555,
        'user_mark': 'MarkType.X',
        'result': None,
        'total_turns': 0,
        'overview': None,
        'started_dttm': '2021-05-31 10:00:00',
        'finished_dttm': None
    }
    assert response.status_code == 200
    create_game_mock.assert_called_once_with(999)


def test_get_game_if_not_found(client):
    response = client.get("/api/v1/games/999")

    assert response.status_code == 404
    assert response.json == {
        'message': 'Game 999 not found. '
                   'You have requested this URI [/api/v1/games/999] '
                   'but did you mean /api/v1/games/<int:game_id> or /api/v1/ or /api/v1/docs ?'
    }


@patch("app.games.views.create_game")
def test_create_new_game(create_game_mock, client, game_x):
    create_game_mock.return_value = game_x
    user_id = 555

    response = client.post("/api/v1/games/", json=dict(user_id=user_id))

    assert response.json == {
        'id': 999,
        'user_id': 555,
        'user_mark': 'MarkType.X',
        'result': None,
        'total_turns': 0,
        'overview': None,
        'started_dttm': '2021-05-31 10:00:00',
        'finished_dttm': None
    }
    assert response.status_code == 201
    create_game_mock.assert_called_once_with(user_id)
