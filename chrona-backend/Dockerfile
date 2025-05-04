FROM python:3.10-slim

# System deps for Poetry and build
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    python3-dev \
    cargo \
    curl \
 && rm -rf /var/lib/apt/lists/*


WORKDIR /app
RUN mkdir -p /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.1.2 \
    PATH="/root/.local/bin:$PATH"

# Setting Up Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
# Install dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Copy rest of the app
COPY . .

# Create non-root user and switch
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER appuser

# Gunicorn as the entrypoint

ENTRYPOINT ["/entrypoint.sh"]

EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
