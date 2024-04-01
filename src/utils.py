import json

from aiohttp import ClientSession
from loguru import logger
from tenacity import retry


@retry
async def get_json(session: ClientSession, url: str) -> json:
    async with session.get(url) as response:
        logger.info(response.status)
        assert response.status == 200
        data = await response.json()
        return data

