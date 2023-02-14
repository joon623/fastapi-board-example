from fastapi import FastAPI

from app.config.connection import database, engine, metadata
from app.routes import user


def create_app() -> FastAPI:
    metadata.create_all(engine)
    app = FastAPI()
    return app


app = create_app()

app.include_router(user.router)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/")
def main():
    return {""}
