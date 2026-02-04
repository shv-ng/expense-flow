# ---- Base image ----
FROM python:3.12-slim

# ---- Environment ----
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1

# ---- Working directory ----
WORKDIR /app

# ---- System deps (keep minimal) ----
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ---- Install uv ----
RUN pip install --no-cache-dir uv

# ---- Copy dependency files first (better caching) ----
COPY pyproject.toml uv.lock* ./

# ---- Install dependencies ----
RUN uv sync --frozen --no-dev

# ---- Copy application code ----
COPY . .

# ---- Expose port ----
EXPOSE 8000

# ---- Run app ----
CMD ["uv", "run", "fastapi", "run" ]

