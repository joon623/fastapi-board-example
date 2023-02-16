from typing import Optional

from pydantic import BaseModel
from pydantic.datetime_parse import datetime


class Board(BaseModel):
    id: Optional[int]
    created_at: Optional[datetime]
    username: Optional[str]
    email: Optional[str]
    title: str
    body: str


class BoardInput(BaseModel):
    title: str
    body: str