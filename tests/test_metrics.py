from fastapi.testclient import TestClient
from main import app

# Test all Metrics tests using the URL and expected score 
# defined with their test_test attribute

endpoint = TestClient(app)


def test_api():
    app.run_tests(endpoint)
