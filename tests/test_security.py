def test_protected_route_requires_authentication(client):
    response = client.get("/usage/")
    assert response.status_code == 401


def test_user_isolation_for_prescriptions(client):
    client.post(
        "/auth/register",
        json={"username": "iso1", "email": "iso1@example.com", "password": "Pass12345"},
    )
    token1 = client.post(
        "/auth/token",
        data={"username": "iso1", "password": "Pass12345"},
    ).json()["access_token"]

    client.post(
        "/auth/register",
        json={"username": "iso2", "email": "iso2@example.com", "password": "Pass12345"},
    )
    token2 = client.post(
        "/auth/token",
        data={"username": "iso2", "password": "Pass12345"},
    ).json()["access_token"]

    upload_resp = client.post(
        "/pipeline/upload",
        headers={"Authorization": f"Bearer {token1}"},
        files={"file": ("doc.jpeg", b"fake-image-bytes", "image/jpeg")},
    )
    assert upload_resp.status_code == 200
    prescription_id = upload_resp.json()["id"]

    forbidden = client.get(
        f"/prescriptions/{prescription_id}",
        headers={"Authorization": f"Bearer {token2}"},
    )
    assert forbidden.status_code == 403


def test_invalid_authentication_token_rejected(client):
    response = client.get(
        "/usage/",
        headers={"Authorization": "Bearer invalidtoken"},
    )
    assert response.status_code == 401
