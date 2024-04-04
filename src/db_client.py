import asyncio

import asyncpg
from asyncpg import Connection

from src.config import DB_URL


async def connection():
    conn: Connection = await asyncpg.connect(DB_URL)
    return conn


async def create_table():
    conn = await connection()
    await conn.execute("""CREATE TABLE IF NOT EXISTS product(
    id BIGSERIAL PRIMARY KEY ,
    product_id varchar(200) unique ,
    name varchar(500),
    brand varchar(500),
    product_type varchar(500),
    price integer,
    description text,
    application text,
    composition text,
    about_brand text,
    addit_information text
    )""")
    await conn.close()


async def data_cleaner():
    conn = await connection()
    await conn.execute("""TRUNCATE TABLE product""")
    await conn.close()


async def insert_data(data: list[tuple]):
    conn = await connection()
    await conn.executemany("""INSERT INTO product (product_id, name, brand, product_type, price, description, application, 
    composition, about_brand, addit_information) 
    VALUES ($1, $2, $3,$4, $5, $6, $7, $8, $9, $10)
    ON CONFLICT (product_id) DO UPDATE SET price = excluded.price""", data)

    count = await conn.fetchval("""SELECT COUNT(*) FROM product""")
    await conn.close()

    return count


async def get_products():
    conn = await connection()
    result = await conn.fetch("""SELECT product_id, name, brand, price, description, application, composition, 
    about_brand, addit_information FROM product""")
    await conn.close()
    return [list(i) for i in result]
