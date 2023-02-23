from sqlalchemy import Table, Integer, Column, DateTime, ForeignKeyConstraint, String, ForeignKey

from app.config.connection import metadata

boards = Table(
    "boards",
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column("created_at",
           DateTime(timezone=True), nullable=False),
    Column("username", ForeignKey("users.username"), nullable=False),
    Column("email", ForeignKey("users.email"), nullable=False),
    Column("title", String(500), nullable=False),
    Column("body", String(2000), nullable=False),
)
