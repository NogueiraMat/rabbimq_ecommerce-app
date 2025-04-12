from typing import Optional, Union
from pydantic import BaseModel


class RequestAuthentication(BaseModel):
    username: str
    password: str


class ResponseAuthentication(BaseModel):
    msg: Optional[str] = None
    error: Optional[str] = None
    data: Union[str, dict]

