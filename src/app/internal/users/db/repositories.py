from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.repository import SQLAlchemyRepository
from app.internal.models import User


class UserRepository(SQLAlchemyRepository):
    model = User

    async def get_user_with_tokens(self, **kwargs) -> User:
        query = (
            select(self.model)
            .filter_by(**kwargs)
            .options(
                selectinload(self.model.tokens),
            )
        )
        result = await self.session.scalar(query)
        return result
