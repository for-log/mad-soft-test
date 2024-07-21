from fastapi import FastAPI, UploadFile, HTTPException

import database
import config
import external
from fastapi.middleware.cors import CORSMiddleware


def validate_file(file: UploadFile):
    if file.content_type not in config.GOOD_TYPES:
        raise HTTPException(status_code=415, detail="Unsupported media type")
    if file.size > config.MAX_SIZE:
        raise HTTPException(status_code=413, detail="File too large")


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    await database.create_tables()


@app.get("/memes")
async def get_memes(last_id: int = 0, limit: int = 10):
    return await database.get_memes(last_id, limit)


@app.get("/memes/{id}")
async def get_meme(id: int):
    return await database.get_meme(id)


@app.post("/memes")
async def create_meme(text: str, file: UploadFile):
    validate_file(file)
    random_name = await external.upload_file(file.file)
    return await database.create_meme(database.Meme(text=text, image=random_name))


@app.put("/memes/{id}")
async def update_meme(id: int, text: str, file: UploadFile):
    validate_file(file)
    random_name = external.upload_file(file.file)
    meme = database.Meme(text=text, image=random_name)
    return await database.update_meme(id, meme)


@app.delete("/memes/{id}")
async def delete_meme(id: int):
    return await database.delete_meme(id)