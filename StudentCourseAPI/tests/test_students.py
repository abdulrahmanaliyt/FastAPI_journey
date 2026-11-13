from app.models.user import User
from app.models.student import Student

def test_create_student_profile(client):

    response = client.post(
        "/students/me",
        json={"name": "Test Student"}
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Test Student"
    assert "id" in response.json()


def test_create_duplicate_student_profile(client):
    first_response = client.post(
        "/students/me",
        json={"name": "Test Student"}
    )
    assert first_response.status_code == 201

    second_response = client.post(
        "/students/me",
        json={"name": "Another Student"}
    )
    assert second_response.status_code == 409


def test_get_my_student_profile(client):
    create_response = client.post(
        "/students/me",
        json={"name": "Test Student"}
    )
    assert create_response.status_code == 201

    response = client.get("/students/me")

    assert response.status_code == 200
    assert response.json()["name"] == "Test Student"


def test_cannot_access_another_users_student(client, db_session):
    other_user = User(
        email="other@example.com",
        password_hash="test_password_hash",
        role="user"
    )

    db_session.add(other_user)
    db_session.commit()
    db_session.refresh(other_user)

    other_student = Student(
        name="Other Student",
        user_id=other_user.id
    )

    db_session.add(other_student)
    db_session.commit()
    db_session.refresh(other_student)

    response = client.get(f"/students/{other_student.id}")

    assert response.status_code == 404
