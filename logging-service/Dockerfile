FROM python:3.11-slim

# Set work directory
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy project files
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && poetry install --no-root
COPY ./app ./app

# Run app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7000"]