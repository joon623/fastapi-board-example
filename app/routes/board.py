import datetime

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from app.crud.board import get_board_item_by_email, create_board_item, delete_board_item_by_id, update_board_item
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
    return await get_board_item_by_email(user_info['email'])


@router.post("/")
async def create_board(content: BoardInput, user_info=Depends(get_user_info)):
    if user_info is not None:
        await create_board_item(datetime=datetime.datetime.now(), username=user_info['username'],
                                email=user_info['email'], title=content.title, body=content.body)
        return JSONResponse(status_code=201, content="ok")


@router.delete("/")
async def delete_board(id: int = Depends(delete_board_by_id)):
    await delete_board_item_by_id(id)
    return JSONResponse(status_code=200, content="ok")


@router.patch("/")
async def update_board(contents=Depends(update_board_by_id)):
    await update_board_item(id=contents["id"], title=contents["title"], body=contents['body'])
    return JSONResponse(status_code=200, content="ok")
