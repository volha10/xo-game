from unittest.mock import patch

from flask.testing import FlaskClient


@patch("app.management.views.start_league")
def test_start_league_response_if_success(
    start_league_mock,
    client: FlaskClient,
    league,
):
    start_league_mock.return_value = league
    new_league_attrs = {"name": "Test League"}

    response = client.post("/api/v1/management/leagues", json=new_league_attrs)

    assert response.json == {
        "id": 1,
        "name": "Test League",
        "started_at": "2021-05-31T10:00:00",
    }
    assert response.status_code == 201


@patch("app.management.views.get_rank_table")
def test_get_rank_table_response_data_if_success(
    get_rank_table,
    client: FlaskClient,
    league_schema,
):
    get_rank_table.return_value = league_schema

    response = client.get(f"/api/v1/management/user-rating")

    assert response.json == {
        "rank_table": [{"rank_number": 1, "user_id": 1, "total_result": 100}]
    }


@patch("app.management.views.get_rank_table")
def test_get_rank_table_response_code_if_success(
    get_rank_table, client: FlaskClient, league_schema
):
    get_rank_table.return_value = league_schema

    response = client.get(f"/api/v1/management/user-rating")

    assert response.status_code == 200


@patch("app.auth.views.get_users")
def test_get_users_response_data_if_success(
    get_users,
    client: FlaskClient,
    users_schema,
):
    get_users.return_value = users_schema

    response = client.get(f"/api/v1/management/users")

    assert response.json == {
        "users": [
            {"link": "http://localhost/api/v1/auth/1"},
        ]
    }


@patch("app.auth.views.get_users")
def test_get_users_response_code_if_success(
    get_users, client: FlaskClient, users_schema
):
    get_users.return_value = users_schema

    response = client.get(f"/api/v1/management/users")

    assert response.status_code == 200
