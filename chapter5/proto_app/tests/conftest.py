import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(scope="function")
def test_client(db_session_test):
    client = TestClient(app)
    yield client
