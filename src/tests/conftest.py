import pytest
import asyncio
from httpx import AsyncClient

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from database import Base
from config import settings


DATABASE_URL = settings.get_db_url(in_docker=False)
SYNC_DATABASE_URL = settings.get_sync_db_url(in_docker=False)


engine = create_engine(SYNC_DATABASE_URL)
sync_session_maker = sessionmaker(engine, expire_on_commit=False)

async_engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
def setup():
    with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE'))

    yield

    engine.dispose()

@pytest.fixture(scope='function')
def clear():
    yield
    with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE'))

@pytest.fixture
def sync_session():
    with sync_session_maker() as session:
        yield session

@pytest.fixture
async def session():
    async with async_session_maker() as session:
        yield session

@pytest.fixture(scope='function')
async def client():
    async with AsyncClient(base_url="http://localhost:8000/api") as client:
        yield client
