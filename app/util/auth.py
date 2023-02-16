import os
from ast import literal_eval
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from passlib.context import CryptContext

from app.config.connection import database
from app.models.user import users
from dotenv import load_dotenv

auth_scheme = HTTPBearer()

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")  # do not use this
ALGORITHM = "HS256"

EXCEPTION_NOT_AUTHORIZATION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email or password",
)

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


def verify_token(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    print(token)
    if token is None:
        raise EXCEPTION_NOT_AUTHORIZATION

    try:
        user_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
    except Exception as e:
        print(e)
        return HTTPException(status_code=400, detail="token is not valid")

    user_sub = literal_eval(user_info['sub'])
    created_at = datetime.strptime(user_sub['created_at'], '%Y-%m-%d %H:%M:%S.%f')
    now = datetime.now()

    if created_at > now:
        return HTTPException(status_code=401, detail="not unauthorized")

    return True


def get_user_info(token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> users:
    try:
        access_token = token.credentials
        user_info = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
    except Exception as e:
        print('get_user_info', e)
        return None

    return user_info


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def get_user_info_in_token(email: str, username: str):
    return {"email": email, "username": username,
            "created_at": str(datetime.now())}


async def get_user(email):
    query = users.select().where(email == users.columns.email)
    return await database.fetch_one(query)


def create_access_token(subject: dict, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: dict, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt
