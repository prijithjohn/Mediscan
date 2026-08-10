FROM python:3.12-slim AS base

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    cargo \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY docker-entrypoint.sh .
COPY . .
RUN chmod +x /app/docker-entrypoint.sh
ENV PYTHONPATH="/app"

FROM base AS backend
WORKDIR /app
EXPOSE 8000
ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM base AS frontend
WORKDIR /app
EXPOSE 8501
CMD ["streamlit", "run", "frontend/app.py", "--server.port", "8501", "--server.address", "0.0.0.0", "--server.headless", "true"]
