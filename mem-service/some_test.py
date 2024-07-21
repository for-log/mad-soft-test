# Архитектура не дает сделать мок БД =(
# Тесты под вопросом

import pytest
from database import create_tables, drop_tables, get_meme, create_meme, delete_meme, Meme


@pytest.mark.asyncio
async def test_create_meme():
    meme = await create_meme(Meme(text="test", image="test.png"))
    assert meme.text == "test" and meme.image == "test.png" and meme.id is not None
    await delete_meme(meme.id)


@pytest.mark.asyncio
async def test_get_meme():
    new_meme = await create_meme(Meme(text="test", image="test.png"))
    meme = await get_meme(new_meme.id)
    assert meme.text == new_meme.text and meme.image == new_meme.image and meme.id == new_meme.id
    await delete_meme(meme.id)


