from fastapi import APIRouter, Depends
from pydantic import BaseModel

from database.db import insert_stock


router = APIRouter()


class RequestStock(BaseModel):
    product_id: int
    quantity: int


@router.post("/stock")
def add_stock(stock_data: RequestStock):
    new_stock = insert_stock(stock_data)
    if new_stock["success"] == False:
        return new_stock
    return new_stock

