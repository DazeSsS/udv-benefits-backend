import sys
sys.dont_write_bytecode = True

import json
import asyncio
from pathlib import Path

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.app.internal.schemas import BenefitSchemaAdd
from src.app.internal.models import Benefit, BenefitContent, Category, Option
from src.config import settings 

DATABASE_URL = settings.get_db_url(in_docker=False)

engine = create_async_engine(DATABASE_URL)

# Categories
async def create_categories(session: AsyncSession):
    with open('data/categories.json', 'r', encoding='utf-8') as file:
        categories_data = json.load(file)

    await session.execute(text('TRUNCATE TABLE category RESTART IDENTITY CASCADE'))
    await session.commit()

    async with session.begin():
        for category in categories_data:
            new_category = Category(**category)
            session.add(new_category)

# Benefits
async def create_benefits(session: AsyncSession):
    with open('data/benefits.json', 'r', encoding='utf-8') as file:
        benefits_data = json.load(file)

    async with session.begin():
        for benefit in benefits_data:
            benefit_schema = BenefitSchemaAdd(**benefit)
            benefit_dict = benefit_schema.model_dump(exclude={'content', 'options'})
            benefit_obj = Benefit(**benefit_dict)
            session.add(benefit_obj)

            await session.flush()

            content_dict = benefit_schema.content.model_dump()
            content_dict.update(benefit_id=benefit_obj.id)
            content_obj = BenefitContent(**content_dict)
            session.add(content_obj)

            if benefit_schema.options:
                for option in benefit_schema.options:
                    option_dict = option.model_dump()
                    option_dict.update(benefit_id=benefit_obj.id)
                    option_obj = Option(**option_dict)
                    session.add(option_obj)

async def populate_db():
    async with AsyncSession(engine) as session:
        await create_categories(session)
        await create_benefits(session)

if __name__ == '__main__':
    asyncio.run(populate_db())
