from unittest.mock import patch

import pytest
from flask.testing import FlaskClient


@pytest.mark.skip(reason="todo")
@patch("app.auth.views.get_user")
def test_get_user_by_id_response_data_if_success(
    get_user_mock,
    client: FlaskClient,
    user_schema,
):
    get_user_mock.return_value = user_schema

    response = client.get(f"/api/v1/auth/1")

    assert response.json == {"id": 1, "options": [{"option_1": "value_1"}]}


@patch("app.auth.views.get_user")
def test_get_user_by_id_response_code_if_success(
    get_user_mock, client: FlaskClient, user_schema
):
    get_user_mock.return_value = user_schema

    response = client.get(f"/api/v1/auth/1")

    assert response.status_code == 200
