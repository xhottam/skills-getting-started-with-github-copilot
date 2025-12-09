import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Unregister first in case already present
    client.delete(f"/activities/{activity}/unregister?email={email}")
    # Signup
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    # Duplicate signup should fail
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400
    # Unregister
    response_unreg = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response_unreg.status_code == 200
    assert "Unregistered" in response_unreg.json()["message"]
    # Unregister again should fail
    response_unreg2 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response_unreg2.status_code == 400
