FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY . .

COPY ./pyproject.toml . 

RUN uv sync

EXPOSE 8000

CMD ["uv", "run", "fastapi", "dev", "main.py", "--port", "8000"]