import asyncio
import json
from funcy import chunks

from aiohttp import ClientSession, ClientTimeout
from loguru import logger
from tenacity import retry

from .config import PAGES_URL
from .models import ProductList, ProductData


# @retry
async def get_json(session: ClientSession, url: str) -> json:
    async with session.get(url) as response:
        assert response.status == 200
        data = await response.json()
        return data


async def get_product_list(session: ClientSession, url: str) -> ProductList:
    data = await get_json(session, url)
    data = data['data']['products']
    return ProductList(**data)


async def get_product_ids(session: ClientSession) -> list:
    ids = []
    start_data = await get_product_list(session, f'{PAGES_URL}0')
    count = start_data.count
    ids.extend(start_data.products)

    if count % 24 == 0:
        last_page = count // 24 + 1
    else:
        last_page = (count // 24) + 2

    tasks = []
    for i in range(1, last_page):
        task = asyncio.create_task(get_product_list(session, f'{PAGES_URL}{i}'))
        tasks.append(task)
        if len(tasks) == 7:
            data = await asyncio.gather(*tasks)
            data = [i.products for i in data]
            data = sum(data, [])
            ids.extend(data)
    else:
        if tasks:
            data = await asyncio.gather(*tasks)
            data = [i.products for i in data]
            data = sum(data, [])
            ids.extend(data)

    return ids


async def get_product_detail(session: ClientSession, url: str) -> tuple:
    data = await get_json(session, url)
    return ProductData(**data['data']).to_tuple()
