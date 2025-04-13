from typing import Optional, Union
from pydantic import BaseModel


class RequestAuthentication(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    firstname: str
    lastname: str
    address: str
    role: str
    access_token: str


class ResponseAuthentication(BaseModel):
    msg: Optional[str] = None
    error: Optional[str] = None
    data: Union[str, UserResponse]

