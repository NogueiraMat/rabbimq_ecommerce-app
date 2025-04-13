from pydantic import BaseModel
from typing import Optional


class RequestUser(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str
    address: str
    role: Optional[str] = "NORMAL"

