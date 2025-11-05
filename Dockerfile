# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# models/ will be copied by the GitHub Action after dvc pull (so ensure it exists)
COPY models/ models/

ENV PORT=8080
EXPOSE 8080

# Use Gunicorn with 1 worker per pod (HPA will scale pods). If you want multiple workers per pod, adjust worker count.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app", "--workers", "1", "--timeout", "120"]

