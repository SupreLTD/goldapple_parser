import asyncio
import json
import os

from funcy import chunks

from aiohttp import ClientSession, ClientTimeout
from loguru import logger
from tenacity import retry
import pandas as pd

from .config import PAGES_URL
from .db_client import get_products
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


async def write_to_excel():
    f = os.path.join(os.path.dirname(__file__), '../data')
    if not os.path.exists(f):
        os.mkdir(f)
    data = await get_products()
    columns = ['id', 'Название товара', 'Бренд', 'Цена', 'Описание', 'Применение', 'Состав', 'О бренде',
               'Дополнительная информация']
    df = pd.DataFrame(data, columns=columns)
    df.to_excel(f'{f}/data.xlsx')

# db_path = os.path.join(os.path.dirname(__file__), '../db.json')
# print(os.path.dirname(__file__))