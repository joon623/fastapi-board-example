import datetime as datetime

from app.config.connection import database
from app.models.boards import boards


async def get_board_item_by_email(email: str):
    query = boards.select().where(boards.c.email == email)
    return await database.fetch_all(query)


async def create_board_item(datetime: datetime, username: str, email: str, title: str, body: str):
    insert_query = boards.insert().values(created_at=datetime, username=username,
                                          email=email, title=title, body=body)
    return await database.execute(insert_query)


async def delete_board_item_by_id(id: int):
    query = boards.delete().where(boards.c.id == id)
    return await database.execute(query)


async def update_board_item(id: int, title: str, body: str):
    query = boards.update().where(boards.c.id == id).values(id=id, title=title, body=body)
    await database.execute(query)
