import requests
from requests.exceptions import RequestException

from frontend import api_client


def test_api_client_has_required_functions():
    assert hasattr(api_client, "health_check")
    assert hasattr(api_client, "register")
    assert hasattr(api_client, "login")
    assert hasattr(api_client, "upload_prescription")
    assert hasattr(api_client, "get_prescriptions")
    assert hasattr(api_client, "get_prescription")
    assert hasattr(api_client, "get_usage")
    assert hasattr(api_client, "get_alerts")
    assert hasattr(api_client, "logout")


def test_parse_invalid_response_raises_api_client_error(monkeypatch):
    class DummyResponse:
        status_code = 200

        def raise_for_status(self):
            return None

        def json(self):
            raise ValueError("Invalid JSON")

    def dummy_request(method, url, timeout, **kwargs):
        return DummyResponse()

    monkeypatch.setattr(api_client.requests, "request", dummy_request)
    try:
        api_client._safe_request("GET", "http://example.com")
        assert False, "Expected ApiClientError"
    except Exception as exc:
        assert isinstance(exc, api_client.ApiClientError)


def test_connection_error_raises_api_client_error(monkeypatch):
    def dummy_request(method, url, timeout, **kwargs):
        raise RequestException("Connection failed")

    monkeypatch.setattr(api_client.requests, "request", dummy_request)
    try:
        api_client._safe_request("GET", "http://example.com")
        assert False, "Expected ApiClientError"
    except Exception as exc:
        assert isinstance(exc, api_client.ApiClientError)
