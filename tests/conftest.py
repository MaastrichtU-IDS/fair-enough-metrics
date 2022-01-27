from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from api.main import app


test_client = TestClient(app)


@pytest.fixture(scope="session")
def test_api():
    with TestClient(app) as test_client:
        yield test_client
