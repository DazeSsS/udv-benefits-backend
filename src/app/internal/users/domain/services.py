from sqlalchemy.ext.asyncio import AsyncSession

from app.internal.users.db.repositories import UserRepository
from app.internal.users.domain.schemas import UserSchemaAdd


class UserService:
    def __init__(
        self,
        user_repo: UserRepository,
        session: AsyncSession,
    ):
        self.user_repo: UserRepository = user_repo(session)

    async def add_user(self, user: UserSchemaAdd):
        user_dict = user.model_dump()
        user = await self.user_repo.add(data=user_dict)
        return user

    async def get_users(self):
        user = await self.user_repo.get_all()
        return user