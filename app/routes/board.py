import datetime

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from app.config.connection import database
from app.models.boards import boards
from app.schema.board import BoardInput
from app.util.auth import verify_token, get_user_info
from app.util.board import delete_board_by_id, update_board_by_id

router = APIRouter(
    prefix="/boards",
    tags=["boards"],
    dependencies=[Depends(verify_token)]
)


@router.get('/')
async def get_board(user_info=Depends(get_user_info)):
    query = boards.select().where(boards.c.email == user_info['email'])
    return await database.fetch_all(query)


@router.post("/")
async def create_board(content: BoardInput, user_info=Depends(get_user_info)):
    if user_info is not None:
        insert_query = boards.insert().values(created_at=datetime.datetime.now(), username=user_info['username'],
                                              email=user_info['email'], title=content.title, body=content.body)
        await database.execute(insert_query)
        return JSONResponse(status_code=201, content="ok")


@router.delete("/")
async def delete_board(id: int = Depends(delete_board_by_id)):
    query = boards.delete().where(boards.c.id == id)
    await database.execute(query)
    return JSONResponse(status_code=200, content="ok")


@router.patch("/")
async def update_board(contents=Depends(update_board_by_id)):
    query = boards.update().where(boards.c.id == contents["id"]).values(title=contents['title'], body=contents['body'])
    await database.execute(query)
    return JSONResponse(status_code=200, content="ok")
