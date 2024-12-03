import sys
import json
import asyncio
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.app.internal.models import Benefit, Category
from src.config import settings 

DATABASE_URL = settings.get_db_url(in_docker=False)

engine = create_async_engine(DATABASE_URL)

# Categories
async def create_categories():
    with open('data/categories.json', 'r', encoding='utf-8') as file:
        categories_data = json.load(file)

    async with AsyncSession(engine) as session:
        async with session.begin():
            for category in categories_data:
                new_category = Category(**category)
                session.add(new_category)

# Benefits
async def create_benefits():
    with open('data/benefits.json', 'r', encoding='utf-8') as file:
        benefits_data = json.load(file)

    async with AsyncSession(engine) as session:
        async with session.begin():
            for benefit in benefits_data:
                new_benefit = Benefit(**benefit)
                session.add(new_benefit)

async def populate_db():
    await create_categories()
    # await create_benefits()

if __name__ == '__main__':
    asyncio.run(populate_db())
