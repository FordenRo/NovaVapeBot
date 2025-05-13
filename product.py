from enum import IntEnum
import json


class ProductType(IntEnum):
    LIQUID = 1
    VAPE = 2
    EVAPE = 3
    SNUS = 4


class Product:
    def __init__(self, product_type: ProductType, brand: str, name: str, cost: float) -> None:
        self.product_type = product_type
        self.brand = brand
        self.name = name
        self.cost = cost

    @classmethod
    def from_json(cls, obj: str):
        obj = json.loads(obj)
        return cls(**obj)
    
    def to_json(self) -> str:
        return json.dumps({'type': self.product_type.value,
                           'brand': self.brand,
                           'name': self.name,
                           'cost': self.cost})


def filter_by_brand(products: list[Product], brand: str):
    return filter(lambda product: product.brand == brand, products)


def filter_by_type(products: list[Product], type: ProductType):
    return filter(lambda product: product.product_type == type, products)


def get_brands(products: list[Product]):
    return list(set(i.brand for i in products))

