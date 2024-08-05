from typing import Annotated
from fastapi import FastAPI, UploadFile, Depends
from fastapi.responses import StreamingResponse
from os import urandom, environ

import repository


def get_minio_repository():
    return repository.MinioRepository(
        url=environ["MINIO_URL"],
        access_key=environ["ACCESS_KEY"],
        secret_key=environ["SECRET_KEY"],
        bucket_name=environ["BUCKET_NAME"],
    )


S3Depend = Annotated[repository.MinioRepository, Depends(get_minio_repository)]
app = FastAPI()


@app.on_event("startup")
def startup():
    get_minio_repository().create_bucket_if_not_exists()


@app.post("/upload")
def upload_image(file: UploadFile, repository: S3Depend):
    random_name = urandom(8).hex()
    repository.upload_file(random_name, file.file, file.size)
    return {"filename": random_name}


@app.get("/download/{filename}")
def get_image(filename: str, repository: S3Depend):
    file = repository.get_file(filename)
    def read_file():
        for chunk in file.stream():
            yield chunk
    return StreamingResponse(read_file())
