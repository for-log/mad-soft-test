from minio import Minio
from os import environ

client = Minio(
    environ.get("MINIO_URL"),
    environ.get("ACCESS_KEY"),
    environ.get("SECRET_KEY"),
    secure=False
)
MAIN_BUCKET = environ.get("BUCKET_NAME")


def create_bucket_if_not_exists():
    if client.bucket_exists(MAIN_BUCKET):
        return
    client.make_bucket(MAIN_BUCKET)


def upload_file(file_name, data, ln):
    client.put_object(MAIN_BUCKET, file_name, data, ln)


def get_file(file_name):
    return client.get_object(MAIN_BUCKET, file_name)