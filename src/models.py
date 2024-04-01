import json

from pydantic import BaseModel, field_validator
from typing import List


class ProductDetail(BaseModel):
    itemId: str


class ProductList(BaseModel):
    count: int
    products: List[ProductDetail]

    @field_validator('products')
    def set_products(cls, value):
        return [i.itemId for i in value]


# with open('test.json', encoding='utf-8') as f:
#     data = json.load(f)
#
# pd_data = ProductList(**data)
# print(pd_data.count)
# print(pd_data.products)
