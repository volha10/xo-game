import pytest

from app import create_app


@pytest.fixture
def test_client():
    app = create_app()
    app.config['TESTING'] = True

    # Create test client using Flask app configured for testing.
    with app.test_client() as test_client_:

        # Establish application context.
        with app.app_context():
            yield test_client_
