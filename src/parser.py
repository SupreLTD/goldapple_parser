import asyncio

from aiohttp import ClientSession, ClientTimeout
from loguru import logger
from pprint import pprint
from random import shuffle
from funcy import chunks
from tqdm import tqdm

from .config import HEADERS, ITEM_URL
from .db_client import insert_data, create_table, data_cleaner
from .utils import get_product_detail, get_product_ids, write_to_excel


async def main():
    await write_to_excel()

    await create_table()
    await data_cleaner()
    async with ClientSession(headers=HEADERS, timeout=ClientTimeout(total=60)) as session:
        ids = await get_product_ids(session)
        shuffle(ids)
        tasks = []
        for chunk in tqdm(list(chunks(7, ids))):
            for i in chunk:
                tasks.append(asyncio.create_task(get_product_detail(session, ITEM_URL % i)))

            products = await asyncio.gather(*tasks)
            count_saved_data = await insert_data(products)
            logger.info(f'Saved {count_saved_data} products')



