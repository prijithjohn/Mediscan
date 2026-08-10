from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.core.config import settings

engine_kwargs = {"future": True}
if settings.database_url == "sqlite:///:memory:":
    engine_kwargs.update({"connect_args": {"check_same_thread": False}, "poolclass": StaticPool})

engine = create_engine(settings.database_url, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
