from sqlalchemy import select, update
from sqlalchemy.orm import joinedload

from app.repository import SQLAlchemyRepository
from app.internal.models import Token


class AuthRepository(SQLAlchemyRepository):
    model = Token

    async def get_token_with_user(self, **kwargs):
        query = (
            select(self.model)
            .filter_by(**kwargs)
            .options(joinedload(self.model.user))
        )
        result = await self.session.scalar(query)
        return result

    async def revoke_tokens_by_user_id(self, user_id: int):
        stmt = (
            update(self.model)
            .where(
                self.model.user_id == user_id,
                self.model.revoked == False
            )
            .values(revoked=True)
        )
        await self.session.execute(stmt)
