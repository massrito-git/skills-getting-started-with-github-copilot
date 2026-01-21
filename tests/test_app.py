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
    assert "Programming Class" in data

def test_signup_valid():
    response = client.post("/activities/Chess%20Club/signup?email=test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up test@example.com for Chess Club" in data["message"]

def test_signup_invalid_activity():
    response = client.post("/activities/Invalid%20Activity/signup?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_signup_already_signed_up():
    # First signup
    client.post("/activities/Programming%20Class/signup?email=duplicate@example.com")
    # Second signup should fail
    response = client.post("/activities/Programming%20Class/signup?email=duplicate@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "Student already signed up for this activity" in data["detail"]

def test_unregister_valid():
    # First signup
    client.post("/activities/Gym%20Class/signup?email=unregister@example.com")
    # Then unregister
    response = client.delete("/activities/Gym%20Class/unregister?email=unregister@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered unregister@example.com from Gym Class" in data["message"]

def test_unregister_not_signed_up():
    response = client.delete("/activities/Basketball/unregister?email=notsigned@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "Student not signed up for this activity" in data["detail"]

def test_unregister_invalid_activity():
    response = client.delete("/activities/Invalid%20Activity/unregister?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_root_redirect():
    response = client.get("/")
    assert response.status_code == 200
    # Since it's a redirect, but TestClient follows redirects by default
    # Actually, RedirectResponse returns 200 with the content
    assert "Mergington High School" in response.text