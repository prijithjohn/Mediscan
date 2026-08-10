import os

from frontend import api_client


def run_frontend_smoke_tests() -> bool:
    expected_funcs = [
        "health_check",
        "register",
        "login",
        "upload_prescription",
        "get_prescriptions",
        "get_prescription",
        "get_usage",
        "get_alerts",
        "logout",
    ]

    missing = [func for func in expected_funcs if not hasattr(api_client, func)]
    if missing:
        print(f"MISSING FRONTEND API CLIENT FUNCTIONS: {missing}")
        return False

    print("Frontend API client functions present.")

    backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
    print(f"Using backend URL: {backend_url}")

    try:
        health = api_client.health_check()
        if isinstance(health, dict) and health.get("status") == "healthy":
            print("Backend health check succeeded.")
            return True
        print(f"Backend health check returned unexpected payload: {health}")
        return False
    except Exception as exc:
        print(f"Backend health check failed: {exc}")
        return False


if __name__ == "__main__":
    success = run_frontend_smoke_tests()
    print(f"PHASE 9 FRONTEND CHECK PASSED: {success}")
    raise SystemExit(0 if success else 1)
