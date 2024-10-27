from abc import ABC, abstractmethod
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def add(self, data):
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def update_by_id(self):
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def add(self, data: dict) -> model:
        obj = self.model(**data)
        self.session.add(obj)
        await self.session.commit()
        return obj

    async def get_by_id(self, id: int) -> model:
        query = select(self.model).where(self.model.id == id)
        result = await self.session.scalar(query)
        return result

    async def get_all(self) -> list[model]:
        query = select(self.model)
        result = await self.session.scalars(query)
        return result.all()

    async def update_by_id(self, id: int, new_data: dict) -> model:
        obj = await self.get_by_id(id)

        for key, value in new_data.items():
            setattr(obj, key, value)

        await self.session.commit()
        return obj

    async def delete_by_id(self, id: int) -> bool:
        obj = await self.get_by_id(id)
        await self.session.delete(obj)
        await self.session.commit()
        return True
