from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

from app.models.user import users

auth_scheme = HTTPBearer()

SECRET_KEY = "b5e703b413ad7decf8ae3ffa7f60a22df17e70bc147447810a0c195c2809996c"  # do not user this
ALGORITHM = "HS256"

EXCEPTION_NOT_AUTHORIZATION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email or password",
)


def verify_token(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    try:
        if token is None:
            raise EXCEPTION_NOT_AUTHORIZATION
        return True
    except Exception as e:
        print('verify_token', e)
        return HTTPException(status_code=500, detail="a")

def get_user_info(token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> users:
    try:
        access_token = token.credentials
        user_info = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
    except Exception as e:
        print('get_user_info', e)
        return None

    return user_info
