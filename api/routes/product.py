from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional

from database.db import insert_product, fetch_products
from ..models.product import RequestProduct


router = APIRouter()


@router.post("/product")
def add_product(product_data: RequestProduct):
    try:
        new_product = insert_product(product_data)
        if new_product["success"] == False:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(new_product),
            )
        return new_product
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )


@router.get(
    "/product",
    description="Passe um valor de ean caso queira buscar um produto específico",
)
def get_product(product_sku: Optional[int] = None):
    try:
        products = fetch_products(product_sku)
        if products["success"] == False:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(products)
            )
        return products
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )

