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


class Description(BaseModel):
    text: str
    content: str


class Actual(BaseModel):
    amount: int


class Price(BaseModel):
    actual: Actual


class Variant(BaseModel):
    itemId: str
    price: Price


class ProductData(BaseModel):
    id: str
    name: str
    brand: str
    productType: str
    productDescription: List[Description]
    variants: List[Variant]
