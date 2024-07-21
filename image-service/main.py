from io import BytesIO
from fastapi import FastAPI, UploadFile
from os import urandom
from starlette.responses import StreamingResponse

import repository

app = FastAPI()


@app.on_event("startup")
def startup():
    repository.create_bucket_if_not_exists()


@app.post("/upload")
def upload_image(file: UploadFile):
    random_name = urandom(8).hex()
    repository.upload_file(random_name, file.file, file.size)
    return {"filename": random_name}


@app.get("/download/{filename}")
def get_image(filename: str):
    file = repository.get_file(filename)
    return StreamingResponse(BytesIO(file.read()))
