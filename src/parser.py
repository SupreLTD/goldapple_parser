import asyncio
import json

from aiohttp import ClientSession
from loguru import logger
from pprint import pprint
from random import shuffle
from funcy import chunks
from tqdm import tqdm

from .config import HEADERS, PAGES_URL
from .db_client import insert_data, create_table, data_cleaner
from .utils import get_product_detail, get_product_ids


async def main():
    await create_table()
    await data_cleaner()
    async with ClientSession(headers=HEADERS) as session:
        ids = await get_product_ids(session)
        shuffle(ids)
        tasks = []
        for chunk in tqdm(list(chunks(7, ids))):
            for i in chunk:
                tasks.append(asyncio.create_task(get_product_detail(session,
                                                                f'https://goldapple.ru/front/api/catalog/product-card?itemId={i}&cityId=0c5b2444-70a0-4932-980c-b4dc0d3f02b5')))

            products = await asyncio.gather(*tasks)
            count_saved_data = await insert_data(products)
            logger.info(f'Saved {count_saved_data} products')


