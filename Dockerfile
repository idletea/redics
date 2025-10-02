FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.8 /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml readme.md ./
COPY redics/ ./redics
RUN --mount=type=cache,target=/root/.cache/uv \
    uv build \
    && uv venv \
    && uv pip install dist/redics*.whl

FROM python:3.12-slim

ENV PATH="/app/.venv/bin:$PATH"
EXPOSE 8000

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv

CMD ["uvicorn", "redics.asgi:app", "--host", "0.0.0.0", "--port", "8000"]
