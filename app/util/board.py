from fastapi import HTTPException


def delete_board_by_id(id: int):
    if id is None:
        raise HTTPException(status_code=422, detail="detail")
    return id


def update_board_by_id(id: int, title: str, body: str):
    return {"id": id, "title": title, "body": body}

