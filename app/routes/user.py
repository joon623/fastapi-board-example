from datetime import datetime, timedelta

from fastapi import APIRouter, Form, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from fastapi.responses import JSONResponse
from ast import literal_eval

from app.config.connection import database
from app.models.user import users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
SECRET_KEY = "b5e703b413ad7decf8ae3ffa7f60a22df17e70bc147447810a0c195c2809996c"  # do not user this
ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


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


@router.post("/login/")
async def login(email: str = Form(), password: str = Form()):
    query = users.select().where(users.columns.email == email)
    user_info = await database.fetch_one(query)
    if user_info is None:
        raise HTTPException(status_code=404, detail="email is not found")

    if not verify_password(password, user_info.password):
        raise HTTPException(status_code=401, detail="password is wrong")

    del user_info[password]
    user_info['created_at'] = str(datetime.now())

    access_token = create_access_token(user_info)
    refresh_token = create_refresh_token(user_info)

    return JSONResponse({"access_token": access_token, "refresh_token": refresh_token}, status_code=200)


@router.post('/signup')
async def sign_up(email: str = Form(), password: str = Form(), username: str = Form()):
    query = users.select().where(users.columns.email == email)
    user_data = await database.fetch_one(query)

    if user_data:
        raise HTTPException(status_code=409, detail="user is already exists")

    hashed_password = get_password_hash(password)
    user_info = {"email": email, "username": username,
                 "created_at": str(datetime.now())}
    access_token = create_access_token(user_info)
    refresh_token = create_refresh_token(user_info)
    insert_query = users.insert().values(email=email, password=hashed_password, username=username,
                                         created_at=datetime.now(), refresh_token=refresh_token)
    await database.execute(insert_query)
    return JSONResponse({"access_token": access_token, "refresh_token": refresh_token}, status_code=201)


@router.post("/refresh")
async def get_new_access_token(refresh_token: str = Header(default=None)):
    try:
        user_info = jwt.decode(refresh_token, SECRET_KEY, ALGORITHM)
    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="a")
    user_sub = literal_eval(user_info['sub'])
    print(user_sub)
    email = user_sub['email']
    created_at = user_sub['created_at']
    print(user_sub['email'])
    print(created_at)

    if email is None:
        return HTTPException(status_code=401, detail="not unauthorized")

    # if created_at

    return ""


@router.get("/users")
async def get_all_users():
    return await database.fetch_all(users.select())
