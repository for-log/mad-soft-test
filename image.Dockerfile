FROM python:3.12-slim
RUN pip install poetry

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install
COPY image-service .

EXPOSE 8001
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "4"]