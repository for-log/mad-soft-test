# Тестовое для MadSoft (Python-разработчик)
# MEMs =)

## Стек
- Nginx
- Docker
- FastApi
- Minio (S3)
- Postgresql

## Функционал (см. http://localhost/docs)
- Добавление мема с текстом
- Обновление мема
- Удаление мема
- Просмотр мемов

## Запуск
1. Установка Docker (https://docs.docker.com/get-docker/)
2. Настройка окружения (см. docker-compose.yml):
    - DATABASE_URL
    - MINIO_URL
    - ACCESS_KEY
    - SECRET_KEY
    - BUCKET_NAME
    - POSTGRES_USER
    - POSTGRES_PASSWORD
    - POSTGRES_DB
    - MINIO_ROOT_USER
    - MINIO_ROOT_PASSWORD
3. ```bash
   # В папке с проектом
   docker compose up
    ```
4. http://localhost/docs