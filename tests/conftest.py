import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["GEMINI_API_KEY"] = ""
os.environ["RAPIDAPI_KEY"] = ""
os.environ["SMTP_HOST"] = ""
os.environ["SMTP_PORT"] = ""
os.environ["SMTP_USERNAME"] = ""
os.environ["SMTP_PASSWORD"] = ""

from backend.app.main import app
from backend.app.db.base import Base
from backend.app.db.session import SessionLocal, engine


Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def clean_db():
    with SessionLocal() as db:
        db.execute(text("DELETE FROM alerts"))
        db.execute(text("DELETE FROM prescriptions"))
        db.execute(text("DELETE FROM usages"))
        db.execute(text("DELETE FROM subscriptions"))
        db.execute(text("DELETE FROM users"))
        db.commit()
    yield
