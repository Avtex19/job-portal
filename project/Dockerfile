# 1. FIX: Use Python 3.12 to match your pyproject.toml requirement
FROM python:3.12-slim

# Copy uv from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set work directory
WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1

# Install Python dependencies
COPY pyproject.toml uv.lock ./

# 2. FIX: Export the lockfile to a format pip understands, then install
# This ensures we use the EXACT versions from your lockfile
RUN uv export --frozen --format=requirements-txt > requirements.txt && uv pip install --system -r requirements.txt

# Copy project source
COPY . .

# (Optional) Default command, though docker-compose usually overrides this
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]