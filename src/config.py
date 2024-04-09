import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str
    pages_url: str
    prod_url: str

    class Config:
        env_file = data_path = os.path.join(os.path.dirname(__file__), '../.env')
        env_file_encoding = 'utf-8'


config = Settings()

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://goldapple.ru/volosy',
    'traceparent': '00-bfe9d1ab908815ab2f17784e4bbcef21-d33a398c6fcd2361-01',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}
