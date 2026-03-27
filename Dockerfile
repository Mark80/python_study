FROM python:3.11-slim

WORKDIR /app

# Install uv (fast) and create venv
RUN pip install --no-cache-dir uv

# Copy dependency files first for better layer caching
COPY pyproject.toml uv.lock ./

# Install runtime dependencies (no dev)
RUN uv sync --frozen --no-dev

# Copy application code
COPY src/ ./src/
COPY sql/ ./sql/

EXPOSE 8000

# Run the API
CMD ["uv", "run", "uvicorn", "src.api.routes:app", "--host", "0.0.0.0", "--port", "8000"]
