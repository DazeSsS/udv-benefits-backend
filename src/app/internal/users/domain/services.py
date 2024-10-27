from sqlalchemy.ext.asyncio import AsyncSession

from app.repository import SQLAlchemyRepository
from app.internal.users.domain.schemas import UserSchemaAdd


class UserService:
    def __init__(
        self,
        user_repo: SQLAlchemyRepository,
        session: AsyncSession,
    ):
        self.user_repo: SQLAlchemyRepository = user_repo(session)

    async def add_user(self, user: UserSchemaAdd):
        user_dict = user.model_dump()
        user = await self.user_repo.add(user_dict)
        return user

    async def get_users(self):
        user = await self.user_repo.get_all()
        return user