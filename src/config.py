DB_URL = 'postgres://postgres:7030908@localhost:5432/postgres'

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

PAGES_URL = 'https://goldapple.ru/front/api/catalog/plp?categoryId=1000003870&cityId=0c5b2444-70a0-4932-980c-b4dc0d3f02b5&geoPolygons[]=EKB-000000347&geoPolygons[]=EKB-000000367&geoPolygons[]=EKB-000000360&geoPolygons[]=EKB-000000356&pageNumber='