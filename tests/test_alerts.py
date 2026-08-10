import pytest

from backend.app.db.models.alert import Alert
from backend.app.db.session import SessionLocal


def test_alert_user_isolation(client):
    from backend.app.services import alert_service

    def stub_send_email(to_email, subject, body, timeout=20):
        return True

    alert_service.send_email = stub_send_email

    client.post(
        "/auth/register",
        json={"username": "alertiso1", "email": "alertiso1@example.com", "password": "Pass12345"},
    )
    token1 = client.post(
        "/auth/token",
        data={"username": "alertiso1", "password": "Pass12345"},
    ).json()["access_token"]

    client.post(
        "/auth/register",
        json={"username": "alertiso2", "email": "alertiso2@example.com", "password": "Pass12345"},
    )
    token2 = client.post(
        "/auth/token",
        data={"username": "alertiso2", "password": "Pass12345"},
    ).json()["access_token"]

    client.post(
        "/pipeline/upload",
        headers={"Authorization": f"Bearer {token1}"},
        files={"file": ("doc.jpeg", b"fake-image-bytes", "image/jpeg")},
    )

    alerts_response = client.get(
        "/alerts/",
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert alerts_response.status_code == 200
    assert alerts_response.json() == []


def test_alert_user_isolation(client):
    from backend.app.services import alert_service

    def stub_send_email(to_email, subject, body, timeout=20):
        return True

    alert_service.send_email = stub_send_email

    client.post(
        "/auth/register",
        json={"username": "alertiso1", "email": "alertiso1@example.com", "password": "Pass12345"},
    )
    token1 = client.post(
        "/auth/token",
        data={"username": "alertiso1", "password": "Pass12345"},
    ).json()["access_token"]

    client.post(
        "/auth/register",
        json={"username": "alertiso2", "email": "alertiso2@example.com", "password": "Pass12345"},
    )
    token2 = client.post(
        "/auth/token",
        data={"username": "alertiso2", "password": "Pass12345"},
    ).json()["access_token"]

    client.post(
        "/pipeline/upload",
        headers={"Authorization": f"Bearer {token1}"},
        files={"file": ("doc.jpeg", b"fake-image-bytes", "image/jpeg")},
    )

    alerts_response = client.get(
        "/alerts/",
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert alerts_response.status_code == 200
    assert alerts_response.json() == []
