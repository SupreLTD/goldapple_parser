import asyncio
import json
import os

from aiohttp import ClientSession
from funcy import chunks
from tenacity import retry
import pandas as pd
from tqdm import tqdm
from loguru import logger

from .config import config
from .db_client import get_products, insert_data
from .models import ProductList, ProductData


@retry
async def get_json(session: ClientSession, url: str) -> json:
    async with session.get(url) as response:
        if not response.ok:
            raise ValueError(f'Response status not 200, {response.status} | {url}')
        data = await response.json()
        return data


async def get_product_list(session: ClientSession, url: str) -> ProductList:
    data = await get_json(session, url)
    data = data['data']['products']
    return ProductList(**data)


async def get_product_ids(session: ClientSession) -> list:
    ids = []

    start_data = await get_product_list(session, f'{config.pages_url}0')
    count = start_data.count
    ids.extend(start_data.products)

    if count % 24 == 0:
        last_page = count // 24 + 1
    else:
        last_page = (count // 24) + 2

    tasks = []
    for i in range(1, last_page):
        task = asyncio.create_task(get_product_list(session, f'{config.pages_url}{i}'))
        tasks.append(task)

        if len(tasks) == 7:
            data = await asyncio.gather(*tasks)
            data = [i.products for i in data]
            data = sum(data, [])
            ids.extend(data)
            tasks = []
    else:
        if tasks:
            data = await asyncio.gather(*tasks)
            data = [i.products for i in data]
            data = sum(data, [])
            ids.extend(data)

    return ids


async def get_product_detail(session: ClientSession, url: str) -> tuple:
    data = await get_json(session, url)
    data = data['data']
    return ProductData(**data).to_tuple()


async def parse_data(session: ClientSession, ids: list) -> None:
    for chunk in tqdm(list(chunks(3, ids))):
        tasks = []
        for i in chunk:
            task = asyncio.create_task(get_product_detail(session, config.prod_url % i))
            tasks.append(task)
        data = await asyncio.gather(*tasks)
        count_saved_data = await asyncio.create_task(insert_data(data))
        logger.info(f'Saved {count_saved_data} products')


async def write_to_excel() -> None:
    src_path = os.path.dirname(__file__)
    data_path = os.path.join(src_path, '../data')
    if not os.path.exists(data_path):
        os.mkdir(data_path)

    data = await get_products()
    columns = ['id', 'Название товара', 'Бренд', 'Тип товара', 'Цена', 'Описание', 'Применение', 'Состав', 'О бренде',
               'Дополнительная информация']

    df = pd.DataFrame(data, columns=columns)
    df.to_excel(f'{data_path}/data.xlsx', index=False, engine='xlsxwriter')
