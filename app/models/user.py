from sqlalchemy import DateTime, String, Integer, Table, Column, ForeignKeyConstraint
from sqlalchemy.dialects.mysql import LONGTEXT

from app.config.connection import metadata

users = Table(
    "users",
    metadata,
    Column('id', Integer, primary_key=True),
    Column("email", String(50), unique=True, nullable=False),
    Column("username", String(50), unique=True, nullable=False),
    Column("password", LONGTEXT),
    Column("created_at", DateTime(timezone=True))
)
