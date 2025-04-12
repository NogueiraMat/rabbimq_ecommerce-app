from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from ..models.authentication import RequestAuthentication, ResponseAuthentication
from database.db import fetch_a_user


router = APIRouter()


@router.post("/authentication")
def authentication(auth_data: RequestAuthentication):
    response = fetch_a_user(auth_data.username)
    if not response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ResponseAuthentication(
                error="User not found!", data={}
            ).model_dump(),
        )

    if response["password"] != auth_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ResponseAuthentication(
                error="Incorrect password!", data={}
            ).model_dump(),
        )
    return JSONResponse(
        content=ResponseAuthentication(
            msg="User authenticated!", data=response
        ).model_dump(),
        status_code=status.HTTP_200_OK,
    )

