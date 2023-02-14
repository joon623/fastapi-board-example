from sqlalchemy import MetaData, create_engine
from databases import Database as db
from app.config.setting import settings
from sqlalchemy_utils import database_exists, create_database


DATABASE_URL = settings.DATABASE_URL

database = db(DATABASE_URL)

metadata = MetaData()

engine = create_engine(
    DATABASE_URL, connect_args={}
)

if not database_exists(engine.url):
    create_database(engine.url)

metadata.create_all(engine)
