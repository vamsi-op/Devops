# Dockerfile
# Build a lightweight Python image for the Flask app.

FROM python:3.11-slim

# Disable .pyc generation and enable real-time logs.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container.
WORKDIR /app

# Copy dependency list first for better Docker layer caching.
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy project files.
COPY app /app/app
COPY templates /app/templates
COPY static /app/static

# Expose Flask application port.
EXPOSE 5000

# Start the Flask application.
CMD ["python", "/app/app/app.py"]
