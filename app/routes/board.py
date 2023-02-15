import datetime
from ast import literal_eval

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse

from app.config.connection import database
from app.models.boards import boards
from app.schema.board import Board
from app.util.auth import verify_token, get_user_info

router = APIRouter(
    prefix="/boards",
    tags=["boards"],
    dependencies=[Depends(verify_token)]
)


def delete_board_by_id(id: int):
    if id is None:
        raise HTTPException(status_code=422, detail="detail")
    return id


def update_board_by_id(id: int, title: str, body: str):
    return {"id": id, "title": title, "body": body}


@router.get('/')
async def get_board():
    return await database.fetch_all(boards.select())


@router.post("/")
async def create_board(content: Board, user_info=Depends(get_user_info)):
    if user_info is not None:
        user_sub = literal_eval(user_info['sub'])
        insert_query = boards.insert().values(created_at=datetime.datetime.now(), username=user_sub['email'],
                                              email=user_sub['username'], title=content.title, body=content.body)
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
    print(contents)
    await database.execute(query)
    return JSONResponse(status_code=200, content="ok")
