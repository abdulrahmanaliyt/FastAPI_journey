
from alembic.util import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Student Course API is running"
    }


def test_get_student_profile_without_authentication():
    response = client.get("/students/me")

    assert response.status_code == 401
