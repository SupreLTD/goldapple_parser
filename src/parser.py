from aiohttp import ClientSession, ClientTimeout
from loguru import logger
from random import shuffle

from .config import HEADERS
from .utils import get_product_ids, write_to_excel, parse_data
from .db_client import data_cleaner, create_table


async def main():
    logger.info('Start parsing..')
    await create_table()
    await data_cleaner()
    async with ClientSession(headers=HEADERS, timeout=ClientTimeout(total=60)) as session:
        logger.info('Getting products ids..')
        ids = await get_product_ids(session)
        logger.info(f'Find {len(ids)} products')
        shuffle(ids)

        await parse_data(session, ids)

    await write_to_excel()

    logger.info('Finish parsing')
