import os

from pydantic_settings import BaseSettings
from pydantic import field_validator


def _default_int(value: str | None, default: int) -> int:
    if value is None or str(value).strip() == "":
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


class Settings(BaseSettings):
    app_name: str = "MediScan API"
    secret_key: str = os.getenv("SECRET_KEY", "changemeplease")
    access_token_expire_minutes: int = 30
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    rapidapi_key: str = os.getenv("RAPIDAPI_KEY", "")
    rapidapi_host: str = os.getenv(
        "RAPIDAPI_HOST", "pen-to-print-handwriting-ocr.p.rapidapi.com"
    )
    email_host: str = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    email_port: int = 587
    email_sender: str = os.getenv("EMAIL_SENDER", "")
    email_password: str = os.getenv("EMAIL_PASSWORD", "")
    free_analysis_limit: int = 5
    smtp_host: str = os.getenv("SMTP_HOST", "")
    smtp_port: int = 0
    smtp_username: str = os.getenv("SMTP_USERNAME", "")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")
    alert_email: str = os.getenv("ALERT_EMAIL", "")

    @field_validator("access_token_expire_minutes", mode="before")
    def parse_access_token_expire_minutes(cls, value):
        return _default_int(value, 30)

    @field_validator("email_port", mode="before")
    def parse_email_port(cls, value):
        return _default_int(value, 587)

    @field_validator("free_analysis_limit", mode="before")
    def parse_free_analysis_limit(cls, value):
        return _default_int(value, 5)

    @field_validator("smtp_port", mode="before")
    def parse_smtp_port(cls, value):
        return _default_int(value, 0)


settings = Settings()
