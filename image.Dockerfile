FROM python:3.12-slim

WORKDIR /app
RUN pip install poetry

COPY pyproject.toml .
COPY poetry.lock .
COPY image-service .
RUN poetry install

EXPOSE 8001
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]