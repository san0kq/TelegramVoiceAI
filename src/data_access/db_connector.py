from asyncio import current_task

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session
from sqlalchemy.engine.url import URL

from config import settings

DATABASE_URL = URL.create(
    drivername='postgresql+asyncpg',
    username=settings.postgres_user,
    password=settings.postgres_password,
    host=settings.postgres_host,
    port=settings.postgres_external_port,
    database=settings.postgres_db
).render_as_string(hide_password=False)


engine = create_async_engine(
    DATABASE_URL,
    query_cache_size=1200,
    pool_size=20,
    max_overflow=200,
    future=True,
    echo=False
)


async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)


db_session = async_scoped_session(async_session_maker, current_task)
