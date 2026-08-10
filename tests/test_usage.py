def test_usage_does_not_consume_on_failed_analysis(client):
    client.post(
        "/auth/register",
        json={"username": "usageuser", "email": "usageuser@example.com", "password": "Pass12345"},
    )
    token = client.post(
        "/auth/token",
        data={"username": "usageuser", "password": "Pass12345"},
    ).json()["access_token"]

    resp_before = client.get(
        "/usage/",
        headers={"Authorization": f"Bearer {token}"},
    )
    used_before = resp_before.json()["used"]

    empty_resp = client.post(
        "/pipeline/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("empty.jpg", b"", "image/jpeg")},
    )
    assert empty_resp.status_code == 400

    resp_after = client.get(
        "/usage/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp_after.json()["used"] == used_before


def test_usage_limit_enforced(client):
    client.post(
        "/auth/register",
        json={"username": "limituser", "email": "limituser@example.com", "password": "Pass12345"},
    )
    token = client.post(
        "/auth/token",
        data={"username": "limituser", "password": "Pass12345"},
    ).json()["access_token"]

    # Use up default limit
    for _ in range(5):
        resp = client.post(
            "/pipeline/upload",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": ("doc.jpeg", b"fake-image-bytes", "image/jpeg")},
        )
        assert resp.status_code == 200

    final_resp = client.post(
        "/pipeline/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("doc.jpeg", b"fake-image-bytes", "image/jpeg")},
    )
    assert final_resp.status_code == 402
