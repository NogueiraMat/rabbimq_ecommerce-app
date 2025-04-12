from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from database.db import insert_user
from ..models.user import RequestUser


router = APIRouter()


@router.post("/user")
def add_user(user_data: RequestUser):
    try:
        response = insert_user(user_data)

        if response["success"] == False:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(response)
            )

        return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )

