import sys
import json
import asyncio
from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.database import Base
from src.config import settings 


DATABASE_URL = settings.get_db_url(in_docker=False)

engine = create_async_engine(DATABASE_URL)

metadata = Base.metadata


async def reflect_metadata():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.reflect)

async def drop_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)

async def flush_db():
    await reflect_metadata()
    await drop_all_tables()
    
if __name__ == '__main__':
    asyncio.run(flush_db())