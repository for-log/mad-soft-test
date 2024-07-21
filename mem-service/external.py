from typing import BinaryIO

from httpx import AsyncClient
from os import environ
import logging

EXTERNAL_API_URL = environ.get("IMAGE_SERVICE")
logger = logging.getLogger(__name__)


async def upload_file(file: BinaryIO):
    try:
        async with AsyncClient(base_url=EXTERNAL_API_URL) as client:
            response = await client.post("/upload", files={"file": file})
            return response.json()['filename']
    except Exception as e:
        logger.error("Ошибка во внешнем сервисе", e)