from sqlalchemy import select, update
from sqlalchemy.orm import joinedload

from app.repository import SQLAlchemyRepository
from app.internal.models import Token


class AuthRepository(SQLAlchemyRepository):
    model = Token

    async def get_token_with_user(self, **kwargs):
        query = (
            select(Token)
            .filter_by(**kwargs)
            .options(joinedload(Token.user))
        )
        result = await self.session.scalar(query)
        return result

    async def revoke_tokens_by_user_id(self, user_id: int):
        stmt = (
            update(Token)
            .where(
                Token.user_id == user_id,
                Token.revoked == False
            )
            .values(revoked=True)
        )
        await self.session.execute(stmt)
