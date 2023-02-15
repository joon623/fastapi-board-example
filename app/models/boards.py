from sqlalchemy import Table, Integer, Column, DateTime, ForeignKeyConstraint, String

from app.config.connection import metadata

boards = Table(
    "boards",
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column("created_at",
           DateTime(timezone=True), nullable=False),
    Column("username", String(50), nullable=False),
    Column("email", String(50), nullable=False),
    Column("title", String(500), nullable=False),
    Column("body", String(2000), nullable=False),
    ForeignKeyConstraint(
        ['email', "username"], ["users.email", "users.username"]
    )
)
