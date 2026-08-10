import os
from typing import Any

import requests
from requests import Response
from requests.exceptions import RequestException, Timeout, HTTPError

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
TIMEOUT = 10


class ApiClientError(Exception):
    def __init__(self, message: str, status_code: int | None = None, details: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.details = details


def _build_url(path: str) -> str:
    return f"{BACKEND_URL.rstrip('/')}{path}"


def _parse_response(response: Response) -> Any:
    try:
        response.raise_for_status()
    except HTTPError as http_exc:
        payload = None
        try:
            payload = response.json()
            detail = payload.get("detail") if isinstance(payload, dict) else None
        except Exception:
            detail = response.text
        raise ApiClientError(
            message=detail or "Backend returned an error.",
            status_code=response.status_code,
            details=payload,
        ) from http_exc

    try:
        return response.json()
    except ValueError as exc:
        raise ApiClientError("Invalid response from backend.") from exc


def _safe_request(method: str, url: str, **kwargs: Any) -> Any:
    try:
        response = requests.request(method, url, timeout=TIMEOUT, **kwargs)
        return _parse_response(response)
    except Timeout as exc:
        raise ApiClientError("Request timed out. Please try again.") from exc
    except RequestException as exc:
        raise ApiClientError("Unable to connect to backend. Please check the server.") from exc


def health_check() -> Any:
    return _safe_request("GET", _build_url("/health"))


def register(username: str, email: str, password: str) -> Any:
    return _safe_request(
        "POST",
        _build_url("/auth/register"),
        json={"username": username, "email": email, "password": password},
    )


def login(username: str, password: str) -> Any:
    return _safe_request(
        "POST",
        _build_url("/auth/token"),
        data={"username": username, "password": password},
    )


def get_current_user(token: str) -> Any:
    return get_usage(token)


def upload_prescription(token: str, file_name: str, file_bytes: bytes, content_type: str) -> Any:
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": (file_name, file_bytes, content_type)}
    return _safe_request("POST", _build_url("/pipeline/upload"), headers=headers, files=files)


def get_prescriptions(token: str) -> Any:
    headers = {"Authorization": f"Bearer {token}"}
    return _safe_request("GET", _build_url("/prescriptions/"), headers=headers)


def get_prescription(token: str, prescription_id: int) -> Any:
    headers = {"Authorization": f"Bearer {token}"}
    return _safe_request(
        "GET",
        _build_url(f"/prescriptions/{prescription_id}"),
        headers=headers,
    )


def get_usage(token: str) -> Any:
    headers = {"Authorization": f"Bearer {token}"}
    return _safe_request("GET", _build_url("/usage/"), headers=headers)


def get_alerts(token: str) -> Any:
    headers = {"Authorization": f"Bearer {token}"}
    return _safe_request("GET", _build_url("/alerts/"), headers=headers)


def logout() -> dict[str, bool]:
    return {"success": True}
