from abc import ABC, abstractmethod
from sqlalchemy import select
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
