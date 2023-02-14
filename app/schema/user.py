from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    id: Optional[int]
    email: str
    username: str
    password: str
    created_at: datetime
    refresh_token: str
