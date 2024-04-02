import asyncio
import json

from aiohttp import ClientSession
from loguru import logger
from pprint import pprint

from .config import HEADERS, PAGES_URL
from .utils import get_product_detail, get_product_ids
from .models import ProductList


async def main():
    async with ClientSession(headers=HEADERS) as session:
        ids = await get_product_ids(session)
        for i in ids:
            data = await get_product_detail(session, f'https://goldapple.ru/front/api/catalog/product-card?itemId={i}&cityId=0c5b2444-70a0-4932-980c-b4dc0d3f02b5')
            pprint(data)
            break


