FROM python:3.13-slim AS base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Flask application image
FROM base AS app

COPY pyproject.toml uv.lock README.md ./
COPY app/ ./app/

RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 5000

CMD ["flask", "--app", "app", "run", "--host=0.0.0.0", "--port=5000"]


# Playwright autotests image
FROM base AS autotests

COPY pyproject.toml uv.lock README.md ./
COPY app/ ./app/

RUN uv sync --frozen --group dev

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app"

RUN uv run playwright install --with-deps chromium

CMD ["uv", "run", "pytest", "app/autotests/tests", "-v"]