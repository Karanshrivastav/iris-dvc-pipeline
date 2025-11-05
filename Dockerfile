# Use small base image
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app and model directory (model will be injected via DVC pull step in CI or included in build)
COPY app.py .
# We expect models/ to exist in repo (DVC pointers). If DVC artifacts are not present during docker build,
# you can dvc pull before building the image in the workflow and COPY them into the image.
COPY models/ models/

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app", "--workers", "1", "--timeout", "120"]
