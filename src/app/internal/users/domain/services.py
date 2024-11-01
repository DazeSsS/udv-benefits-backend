from sqlalchemy.ext.asyncio import AsyncSession

from app.internal.users.db.repositories import UserRepository
from app.internal.users.domain.schemas import UserSchemaAdd, UserSchemaUpdate


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

    async def get_unverified_users(self):
        unverified_users = await self.user_repo.get_all_by_fields(is_verified=False)
        return unverified_users

    async def get_user_by_id(self, user_id):
        user = await self.user_repo.get_by_id(id=user_id)
        return user

    async def update_user_by_id(self, user_id: int, new_data: UserSchemaUpdate):
        new_data_dict = new_data.model_dump(exclude_unset=True)
        updated_user = await self.user_repo.update_by_id(id=user_id, new_data=new_data_dict)
        return updated_user
