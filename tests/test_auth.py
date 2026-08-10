from backend.app.db.session import SessionLocal
from backend.app.db.models.user import User
from backend.app.services.auth_service import verify_password


def test_register_and_login_success(client):
    register_response = client.post(
        "/auth/register",
        json={"username": "authuser", "email": "authuser@example.com", "password": "Pass12345"},
    )
    assert register_response.status_code == 200
    token = register_response.json().get("access_token")
    assert token

    login_response = client.post(
        "/auth/token",
        data={"username": "authuser", "password": "Pass12345"},
    )
    assert login_response.status_code == 200
    assert login_response.json().get("access_token")

    protected_response = client.get(
        "/usage/",
        headers={"Authorization": f"Bearer {login_response.json().get('access_token')}"},
    )
    assert protected_response.status_code == 200


def test_duplicate_registration_rejected(client):
    client.post(
        "/auth/register",
        json={"username": "duplicateuser", "email": "duplicate@example.com", "password": "Pass12345"},
    )
    duplicate_response = client.post(
        "/auth/register",
        json={"username": "duplicateuser", "email": "duplicate2@example.com", "password": "Pass12345"},
    )
    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["detail"] == "Username already registered"


def test_login_failure(client):
    response = client.post(
        "/auth/token",
        data={"username": "unknownuser", "password": "WrongPass"},
    )
    assert response.status_code == 401


def test_password_hashing_stores_hash(client):
    client.post(
        "/auth/register",
        json={"username": "hashuser", "email": "hashuser@example.com", "password": "Pass12345"},
    )
    with SessionLocal() as db:
        user = db.query(User).filter(User.username == "hashuser").first()
        assert user is not None
        assert user.password_hash != "Pass12345"
        assert verify_password("Pass12345", user.password_hash)
