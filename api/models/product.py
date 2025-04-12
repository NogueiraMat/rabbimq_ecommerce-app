from pydantic import BaseModel


class RequestProduct(BaseModel):
    sku: int
    name: str
    description: str
    price: float

