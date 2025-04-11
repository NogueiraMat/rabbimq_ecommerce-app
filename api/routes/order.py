from fastapi.responses import JSONResponse
from fastapi import APIRouter, status, HTTPException

from database.db import fetch_order, fetch_order_item
from workers.create_order_worker import create_order
from ..models.order import RequestOrder


router = APIRouter()


@router.post("/order")
def add_order(order: RequestOrder):
    try:
        response = create_order(order_data=order.model_dump_json())
        if response["success"] == False:
            return HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(response)
            )
        return JSONResponse(
            content={
                "msg": "order created successfully!",
                "order": response["order_id"],
            },
            status_code=status.HTTP_201_CREATED,
        )
    except HTTPException as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/order")
def get_order():
    try:
        result = fetch_order()
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    except HTTPException as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/order/{order_id}")
def get_order_item(order_id: str):
    try:
        result = fetch_order_item(order_id)
        return JSONResponse(content=result, status_code=status.HTTP_200_OK)
    except HTTPException as e:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

