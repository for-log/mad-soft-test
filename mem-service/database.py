from contextlib import asynccontextmanager
from os import environ
from typing import AsyncGenerator, Optional

from sqlmodel import SQLModel, Field, select
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(environ.get("DATABASE_URL"))


class Meme(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    text: str
    image: str = Field(unique=True, index=True)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        yield session


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


async def get_memes(last_id: int = 0, limit: int = 10) -> list[Meme]:
    async with get_session() as session:
        query = await session.exec(select(Meme).where(Meme.id > last_id).limit(limit))
        return query.all()


async def create_meme(meme: Meme) -> Meme:
    async with get_session() as session:
        session.add(meme)
        await session.commit()
        await session.refresh(meme)
    return meme


async def get_meme(id: int) -> Meme:
    async with get_session() as session:
        return await session.get(Meme, id)


async def update_meme(id: int, meme: Meme) -> Optional[Meme]:
    async with get_session() as session:
        old_meme = await session.get(Meme, id)
        if not old_meme:
            return None

        old_meme.text = meme.text
        old_meme.image = meme.image
        session.add(old_meme)
        await session.commit()
        await session.refresh(old_meme)
    return old_meme


async def delete_meme(id: int) -> Meme:
    async with get_session() as session:
        meme = await session.get(Meme, id)
        await session.delete(meme)
        await session.commit()
    return meme