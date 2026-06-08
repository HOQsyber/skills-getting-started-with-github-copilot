import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))
from app import app, activities

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Arrange: Reset activities to clean state before each test"""
    original = {
        name: {**data, "participants": list(data["participants"])}
        for name, data in activities.items()
    }
    yield
    activities.clear()
    activities.update(original)


# ── GET /activities ──────────────────────────────────────────

def test_get_activities_returns_200():
    """Arrange-Act-Assert: GET /activities returns 200"""
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200


def test_get_activities_returns_dict():
    """Assert response is a dictionary with activity names"""
    response = client.get("/activities")
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


# ── POST /activities/{name}/signup ───────────────────────────

def test_signup_success():
    """Arrange-Act-Assert: Valid signup returns 200 and success message"""
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]


def test_signup_duplicate_returns_400():
    """Assert: Signing up twice returns 400"""
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_invalid_activity_returns_404():
    """Assert: Unknown activity returns 404"""
    # Arrange
    email = "someone@mergington.edu"
    # Act
    response = client.post("/activities/FakeActivity/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_signup_adds_participant():
    """Assert: Participant appears in activity list after signup"""
    # Arrange
    email = "newkid@mergington.edu"
    activity = "Swimming Team"
    # Act
    client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    response = client.get("/activities")
    participants = response.json()[activity]["participants"]
    assert email in participants