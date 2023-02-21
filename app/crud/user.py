from datetime import datetime

from app.config.connection import database
from app.models.user import users


async def get_user_by_email(email: str):
    query = users.select().where(users.columns.email == email)
    return await database.fetch_one(query)


async def get_user_by_username(username: str):
    username_query = users.select().where(users.columns.username == username)
    return await database.fetch_one(username_query)


async def create_user(email: str, hashed_password: str, username: str, created_at: datetime):
    insert_query = users.insert().values(email=email, password=hashed_password, username=username,
                                         created_at=created_at)
    await database.execute(insert_query)
