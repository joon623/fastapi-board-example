import sqlalchemy
from sqlalchemy import DateTime, String, Integer
from sqlalchemy.dialects.mysql import LONGTEXT

from app.config.connection import metadata

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column('id', Integer, primary_key=True, index=True),
    sqlalchemy.Column("email", String(50), unique=True),
    sqlalchemy.Column("username", String(50)),
    sqlalchemy.Column("password", LONGTEXT),
    sqlalchemy.Column("created_at", DateTime(timezone=True)),
    sqlalchemy.Column("refresh_token", LONGTEXT)
)
