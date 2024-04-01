import asyncio
import json

from aiohttp import ClientSession
from loguru import logger
from pprint import pprint

from .config import HEADERS, PAGES_URL
from .utils import get_json
from .models import ProductList


async def main():
    ids = []
    async with ClientSession(headers=HEADERS) as session:
        start_data = await get_json(session, f'{PAGES_URL}1')
        start_data = start_data['data']['products']
        start_data = ProductList(**start_data)
        count = start_data.count
        ids.extend(start_data.products)

        if count % 24 == 0:
            last_page = count // 24 + 1
        else:
            last_page = (count // 24) + 2

        tasks = []
        for i in range(2, last_page):
            task = asyncio.create_task(get_json(session, f'{PAGES_URL}{i}'))
            tasks.append(task)

        data = await asyncio.gather(*tasks)
        data = [ProductList(**i['data']['products']) for i in data]
        data = [i.products for i in data]
        data = sum(data, [])
        ids.extend(data)
