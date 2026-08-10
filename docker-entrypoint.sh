#!/usr/bin/env sh
set -e

export PYTHONPATH="/app"

if [ -z "$DATABASE_URL" ]; then
  echo "ERROR: DATABASE_URL is not set"
  exit 1
fi

echo "Waiting for database availability..."
until python - <<'PY'
import os, sys
from sqlalchemy import create_engine, text

try:
    engine = create_engine(os.environ['DATABASE_URL'])
    with engine.connect() as conn:
        conn.execute(text('SELECT 1'))
except Exception as exc:
    print(exc, file=sys.stderr)
    sys.exit(1)
PY
do
  sleep 1
done

echo "Applying database migrations..."
alembic upgrade head

exec "$@"
