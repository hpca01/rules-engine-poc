FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY . .

COPY ./pyproject.toml . 

RUN uv sync

EXPOSE 80

CMD ["uv", "run", "fastapi", "run", "main.py", "--port", "80"]
