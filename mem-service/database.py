from contextlib import asynccontextmanager
from dataclasses import dataclass
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
async def meme_repository() -> AsyncGenerator["MemeRepository", None]:
    async with AsyncSession(engine) as session:
        yield MemeRepository(session)


async def get_meme_repository() -> "MemeRepository":
    async with meme_repository() as meme_repo:
        return meme_repo


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@dataclass
class MemeRepository:
    session: AsyncSession

    async def get_memes(self, last_id: int, limit: int) -> list[Meme]:
        query = await self.session.exec(
            select(Meme).where(Meme.id > last_id).order_by(Meme.id).limit(limit)
        )
        return query.all()

    async def create_meme(self, meme: Meme) -> Meme:
        self.session.add(meme)
        await self.session.commit()
        await self.session.refresh(meme)
        return meme

    async def get_meme(self, id: int) -> Meme:
        return await self.session.get(Meme, id)

    async def update_meme(self, id: int, meme: Meme) -> Optional[Meme]:
        old_meme = await self.session.get(Meme, id)
        if not old_meme:
            return None

        old_meme.text = meme.text
        old_meme.image = meme.image
        self.session.add(old_meme)
        await self.session.commit()
        await self.session.refresh(old_meme)
        return old_meme

    async def delete_meme(self, id: int) -> Meme:
        meme = await self.session.get(Meme, id)
        await self.session.delete(meme)
        await self.session.commit()
        return meme
