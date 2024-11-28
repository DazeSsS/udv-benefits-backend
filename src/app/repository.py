from abc import ABC, abstractmethod
from sqlalchemy import asc, desc, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyRepository:
    model = None

    def __init__(self, session: AsyncSession):
        self.session : AsyncSession = session

    async def add(self, data: dict) -> model:
        obj = self.model(**data)

        self.session.add(obj)
        await self.session.commit()
        return obj

    async def get_by_id(self, id: int) -> model:
        query = select(self.model).where(self.model.id == id)
        result = await self.session.scalar(query)
        return result

    async def get_one_by_fields(self, **kwargs) -> model:
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.scalar(query)
        return result

    async def get_all_by_fields(self, **kwargs) -> list[model]:
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.scalars(query)
        return result.all()

    async def get_all(self) -> list[model]:
        query = select(self.model)
        result = await self.session.scalars(query)
        return result.all()

    async def get_all_sorted(self, sort_field: str, ascending: bool = True) -> list[model]:
        field = getattr(self.model, sort_field, None)
        if field is None:
            raise ValueError(f'Field "{sort_field}" does not exist in model "{self.model.__name__}".')

        order_by_field = asc(field) if ascending else desc(field)

        query = select(self.model).order_by(order_by_field)
        result = await self.session.scalars(query)
        return result.all()

    async def update_by_id(self, id: int, new_data: dict) -> model:
        obj = await self.get_by_id(id)

        for key, value in new_data.items():
            setattr(obj, key, value)

        await self.session.commit()
        return obj

    async def delete_by_id(self, id: int) -> None:
        obj = await self.get_by_id(id)
        await self.session.delete(obj)
        await self.session.commit()
        return
