import json
import os

from pydantic import BaseModel, field_validator, Field
from typing import List, Any


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

    @field_validator('price')
    def set_price(cls, value: Price):
        return value.actual.amount


class ProductData(BaseModel):
    id: str
    name: str
    brand: str
    productType: str
    productDescription: List[Description]
    variants: List[Variant]

    price: int = Field(default=0)
    description: str = Field(default='')
    application: str = Field(default='')
    composition: str = Field(default='')
    about_brand: str = Field(default='')
    addit_information: str = Field(default='')

    def model_post_init(self, __context: Any) -> None:
        self.price = int(next((variant.price for variant in self.variants if variant.itemId == self.id), ''))
        # for desc in self.productDescription:
        #     if desc.text == 'описание':
        #         self.description = desc.content
        #     elif desc.text == 'применение':
        #         self.application = desc.content
        #     elif desc.text == 'состав':
        #         self.composition = desc.content
        #     elif desc.text == 'о бренде':
        #         self.about_brand = desc.content
        #     elif desc.text == 'Дополнительная информация':
        #         self.addit_information = desc.content

        attributes_mapping = {
            'описание': 'description',
            'применение': 'application',
            'состав': 'composition',
            'о бренде': 'about_brand',
            'Дополнительная информация': 'addit_information'
        }

        for desc in self.productDescription:
            attribute_name = attributes_mapping.get(desc.text)
            if attribute_name:
                setattr(self, attribute_name, desc.content)

        del self.__dict__['variants']
        del self.__dict__['productDescription']

    def to_tuple(self) -> tuple:
        return tuple(self.__dict__.values())

# with open('test.json', encoding='utf-8') as f:
#     data = json.load(f)
#
# data = ProductData(**data['data'])
# data.model_post_init('some')
# print(data.model_post_init.__dir__())

# print(os.path.dirname(__file__))
# print(os.path.exists('test.py'))