
from alembic.util import status
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "success": True,
        "message": "Student Course API is running",
        "data": None
    }

def test_get_student_profile_without_authentication():
    response = client.get("/students/me")

    assert response.status_code == 401
