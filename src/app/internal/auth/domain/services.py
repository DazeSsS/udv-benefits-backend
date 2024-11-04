import jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import BackgroundTasks

from app.email_client import EmailClient
from app.internal.models import User
from app.internal.repositories import AuthRepository, UserRepository
from app.internal.auth.domain.schemas import TokenPairSchema, TokenSchemaAdd

from config import settings

from app.internal.models import User


class AuthService:
    def __init__(
        self,
        auth_repo: AuthRepository,
        user_repo: UserRepository,
        email_client: EmailClient,
        session: AsyncSession,
    ):
        self.auth_repo: AuthRepository = auth_repo(session)
        self.user_repo: UserRepository = user_repo(session)
        self.email_client: EmailClient = email_client()

    @staticmethod
    def get_payload(token: str):
        payload = jwt.decode(
            jwt=token,
            key=settings.JWT_SECRET,
            algorithms=settings.JWT_ALGORITHM
        )
        return payload

    @staticmethod
    def create_jwt(payload: dict, lifetime: timedelta):
        token = jwt.encode(
            payload={
                'exp': datetime.now(timezone.utc) + lifetime,
                **payload
            },
            key=settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )
        return token

    async def revoke_tokens(self, user_id: int):
        await self.auth_repo.revoke_tokens_by_user_id(user_id=user_id)

    async def create_tokens(self, user: User):
        payload = {
            'user_id': user.id,
            'is_admin': user.is_admin,
        }

        access_token = self.create_jwt(payload=payload, lifetime=settings.ACCESS_LIFETIME)
        refresh_token = self.create_jwt(payload={}, lifetime=settings.REFRESH_LIFETIME)

        await self.auth_repo.add(jti=refresh_token, user_id=user.id)

        return TokenPairSchema(access_token=access_token, refresh_token=refresh_token)

    async def refresh_tokens(self, refresh_token: str):
        token = await self.auth_repo.get_token_with_user(jti=refresh_token)

        if token is None:
            return # TODO

        if token.revoked:
            return # TODO

        user = token.user
        await self.revoke_tokens(user.id)

        try:
            self.get_payload(token=token.jti)
        except jwt.ExpiredSignatureError:
            return # TODO

        token_pair = await self.create_tokens(user)
        return token_pair

    async def login(self, token: str):
        try:
            payload = self.get_payload(token=token)
            user_id = payload.get('user_id')
        except jwt.InvalidTokenError:
            return # TODO

        user = await self.user_repo.get_by_id(id=user_id)

        token_pair = await self.create_tokens(user=user)
        return token_pair

    async def send_email(self, user: User, background_tasks: BackgroundTasks):
        jwt_token = self.create_jwt(payload={'user_id': user.id}, lifetime=timedelta(minutes=5))

        background_tasks.add_task(
            self.email_client.send_email,
            recipient_list=[user.email],
            subject='Вход в аккаунт Кафетерий льгот UDV',
            text=(
                f'Поздравляем, {user.first_name}, ваш аккаунт был успешно зарегистрирован в Кафетерии льгот UDV!\n\n'
                f'Для авторизации перейдите по ссыллке: {settings.AUTH_URL + jwt_token}'
            ),
            html=(
                f'<b>Поздравляем, {user.first_name}, ваш аккаунт был успешно зарегистрирован на Кафетерии льгот UDV!</b><br><br>'
                f'<a href="{settings.AUTH_URL + jwt_token}">АВТОРИЗОВАТЬСЯ</a>'
            ),
        )
