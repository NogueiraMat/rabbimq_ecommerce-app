from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status
import secrets


security = HTTPBasic()


def require_admin_user(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = "admin"
    correct_password = "admin"

    is_valid_user = secrets.compare_digest(credentials.username, correct_username)
    is_valid_pass = secrets.compare_digest(credentials.password, correct_password)

    if not (is_valid_user and is_valid_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username

