from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class OrderProductModel(BaseModel):
    id: int
    quantity: int
    price: float


class RequestOrder(BaseModel):
    created_at: Optional[datetime] = datetime.now()
    client_id: int
    order_item_list: list[OrderProductModel]

