from os import environ
import pytest
import asyncio

# So bad...
# Whatever, need connect to inmemory db
environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
from database import Meme, meme_repository, create_tables, drop_tables

MEMES = [
    Meme(text="test", image="test.png"),
    Meme(text="test2", image="test2.png"),
    Meme(text="test3", image="test3.png"),
]


async def startup_tests():
    await create_tables()
    async with meme_repository() as meme_repo:
        meme_repo.session.add_all(MEMES)
        await meme_repo.session.commit()
        for meme in MEMES:
            await meme_repo.session.refresh(meme)


@pytest.fixture(scope="module", autouse=True)
def generated_repo():
    asyncio.run(startup_tests())
    yield
    asyncio.run(drop_tables())


@pytest.mark.asyncio
async def test_create_meme(generated_repo):
    async with meme_repository() as meme_repo:
        meme = await meme_repo.create_meme(Meme(text="test", image="test4.png"))
    assert (
        meme.text == "test" and meme.image == "test4.png" and meme.id == len(MEMES) + 1
    )


@pytest.mark.asyncio
async def test_delete_meme(generated_repo):
    async with meme_repository() as meme_repo:
        meme = await meme_repo.delete_meme(len(MEMES) + 1)
    assert (
        meme.text == "test" and meme.image == "test4.png" and meme.id == len(MEMES) + 1
    )


@pytest.mark.asyncio
async def test_get_meme(generated_repo):
    async with meme_repository() as meme_repo:
        meme = await meme_repo.get_meme(1)
    assert meme.text == MEMES[0].text and meme.image == MEMES[0].image and meme.id == 1


@pytest.mark.asyncio
async def test_get_memes(generated_repo):
    async with meme_repository() as meme_repo:
        memes = await meme_repo.get_memes(0, 10)
    assert len(memes) == 3
    assert memes == MEMES
