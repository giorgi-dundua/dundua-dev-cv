# Use a lightweight Python image
FROM python:3.11-slim

# Prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevent Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd --create-home --uid 10001 appuser

# Copy the application code
COPY --chown=appuser:appuser . .

USER appuser

# Expose the port Fly.io expects
EXPOSE 8080

# Run with Gunicorn (Production Server)
# Access the 'app' object inside 'run.py' (or create_app directly)
CMD ["gunicorn", "--no-control-socket", "--bind", "0.0.0.0:8080", "run:app"]