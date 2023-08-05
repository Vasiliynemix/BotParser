from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str
    sale: int
    salePriceU: float
    brand: str
    feedbacks: int
    reviewRating: float
    volume: int


class Items(BaseModel):
    products: list[Item]
