import pytest

from backend.app.services.auth_service import authenticate_user, register_user
from backend.app.db.models.user import User
from backend.app.db.session import SessionLocal


@pytest.fixture
def user_token(client):
    client.post(
        "/auth/register",
        json={"username": "presuser", "email": "presuser@example.com", "password": "Pass12345"},
    )
    login_resp = client.post(
        "/auth/token",
        data={"username": "presuser", "password": "Pass12345"},
    )
    return login_resp.json()["access_token"]


def test_upload_valid_prescription_consumes_usage(client, user_token):
    response = client.post(
        "/pipeline/upload",
        headers={"Authorization": f"Bearer {user_token}"},
        files={"file": ("doc.jpeg", b"fake-image-bytes", "image/jpeg")},
    )
    assert response.status_code == 200
    assert response.json()["original_text"]
    usage_resp = client.get(
        "/usage/",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert usage_resp.json()["used"] == 1


def test_upload_empty_file_rejected_and_no_usage(client, user_token):
    response = client.post(
        "/pipeline/upload",
        headers={"Authorization": f"Bearer {user_token}"},
        files={"file": ("empty.jpeg", b"", "image/jpeg")},
    )
    assert response.status_code == 400
    usage_resp = client.get(
        "/usage/",
        headers={"Authorization": f"Bearer {user_token}"},
    )
    assert usage_resp.json()["used"] == 0


def test_upload_oversized_file_rejected(client, user_token):
    response = client.post(
        "/pipeline/upload",
        headers={"Authorization": f"Bearer {user_token}"},
        files={"file": ("big.jpeg", b"x" * (5 * 1024 * 1024 + 1), "image/jpeg")},
    )
    assert response.status_code == 413


@pytest.mark.parametrize("content_type", ["image/gif", "text/plain"])
def test_upload_invalid_file_type_rejected(client, user_token, content_type):
    response = client.post(
        "/pipeline/upload",
        headers={"Authorization": f"Bearer {user_token}"},
        files={"file": ("badfile", b"fake", content_type)},
    )
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]
