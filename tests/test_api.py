import sys
import pathlib
from fastapi.testclient import TestClient

# Ensure src is importable
ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC_PATH = str(ROOT / "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from app import app  # import app from src/app.py

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "test.student@mergington.edu"

    # Ensure test email isn't already registered
    resp = client.get("/activities")
    assert resp.status_code == 200
    participants = resp.json()[activity]["participants"]
    if email in participants:
        r = client.post(f"/activities/{activity}/unregister?email={email}")
        assert r.status_code == 200

    # Sign up
    r = client.post(f"/activities/{activity}/signup?email={email}")
    assert r.status_code == 200
    assert "Signed up" in r.json().get("message", "")

    # Confirm present
    resp = client.get("/activities")
    assert email in resp.json()[activity]["participants"]

    # Unregister
    r = client.post(f"/activities/{activity}/unregister?email={email}")
    assert r.status_code == 200
    assert "Unregistered" in r.json().get("message", "")

    # Confirm removed
    resp = client.get("/activities")
    assert email not in resp.json()[activity]["participants"]
