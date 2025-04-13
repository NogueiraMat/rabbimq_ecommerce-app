from datetime import datetime, timedelta
from typing import Union
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
import jwt

SECRET_KEY = "b9afbeb5e54b396089a4b21d6a3e1a713bbbb29bd192269690237c3785081532"
ALGORITHM = "HS256"


def create_access_token(payload: dict, expiry: Union[timedelta, None] = None):
    data_to_encode = payload.copy()

    expires = (
        datetime.now() + timedelta(hours=24) if not expiry else datetime.now() + expiry
    )

    data_to_encode["exp"] = expires

    return jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)


def validate_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError as e:
        return None
    except ExpiredSignatureError as e:
        return None

