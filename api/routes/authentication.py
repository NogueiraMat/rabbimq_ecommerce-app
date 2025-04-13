from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import json

from ..models.authentication import (
    RequestAuthentication,
    ResponseAuthentication,
    UserResponse,
)
from utils.security import create_access_token, validate_access_token
from database.db import fetch_a_user


router = APIRouter()


@router.post("/authentication")
def authentication(auth_data: RequestAuthentication):
    finded_username = fetch_a_user(auth_data.username)
    if not finded_username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ResponseAuthentication(
                error="User not found!", data={}
            ).model_dump(),
        )

    access_token = create_access_token(
        {
            "sub": json.dumps(
                {"user": finded_username["username"], "role": finded_username["role"]}
            )
        }
    )

    return JSONResponse(
        content=ResponseAuthentication(
            msg="Login successfuly!",
            data=UserResponse(
                id=finded_username["id"],
                username=finded_username["username"],
                firstname=finded_username["firstname"],
                lastname=finded_username["lastname"],
                address=finded_username["address"],
                role=finded_username["role"],
                access_token=access_token,
            ),
        ).model_dump(),
        status_code=status.HTTP_200_OK,
    )

