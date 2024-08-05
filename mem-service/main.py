from typing import Annotated
from fastapi import FastAPI, UploadFile, HTTPException, Depends

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
MemeRepoDepend = Annotated[
    database.MemeRepository, Depends(database.get_meme_repository)
]


@app.on_event("startup")
async def on_startup():
    await database.create_tables()


@app.get("/memes")
async def get_memes(meme_repo: MemeRepoDepend, last_id: int = 0, limit: int = 10):
    return await meme_repo.get_memes(last_id, limit)


@app.get("/memes/{id}")
async def get_meme(meme_repo: MemeRepoDepend, id: int):
    return await meme_repo.get_meme(id)


@app.post("/memes")
async def create_meme(meme_repo: MemeRepoDepend, text: str, file: UploadFile):
    validate_file(file)
    random_name = await external.upload_file(file.file)
    return await meme_repo.create_meme(database.Meme(text=text, image=random_name))


@app.put("/memes/{id}")
async def update_meme(meme_repo: MemeRepoDepend, id: int, text: str, file: UploadFile):
    validate_file(file)
    random_name = external.upload_file(file.file)
    meme = database.Meme(text=text, image=random_name)
    return await meme_repo.update_meme(id, meme)


@app.delete("/memes/{id}")
async def delete_meme(meme_repo: MemeRepoDepend, id: int):
    return await meme_repo.delete_meme(id)
