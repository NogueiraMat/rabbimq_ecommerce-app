from pydantic import BaseModel


class RequestUser(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str
    address: str

