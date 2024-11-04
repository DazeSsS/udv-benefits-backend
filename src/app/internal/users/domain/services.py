import os
import json

from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.email_client import EmailClient
from app.internal.repositories import UserRepository
from app.internal.users.db.models import Position
from app.internal.orders.db.models import Status
from app.internal.users.domain.schemas import UserSchemaAdd, UserSchemaUpdate

from config import settings


class UserService:
    def __init__(
        self,
        user_repo: UserRepository,
        email_client: EmailClient,
        session: AsyncSession,
    ):
        self.user_repo: UserRepository = user_repo(session)
        self.email_client: EmailClient = email_client()
        self.users_file: str = settings.USERS_FILE_DIR + 'users.json'
        self.users_prepared_file: str = settings.USERS_FILE_DIR + 'users_prepared.json'

    def prepare_users(self):
        with open(self.users_file, 'r') as file:
            users = json.load(file)

        users_prepared = {}
        for user in users:
            users_prepared[user.get('email')] = user

        with open(self.users_prepared_file, 'w') as file:
            json.dump(users_prepared, file, indent=4, ensure_ascii=False)

    async def check_users_file(self, email: str):        
        if not os.path.exists(self.users_file):
            return None

        if not os.path.exists(self.users_prepared_file):
            self.prepare_users()

        with open(self.users_prepared_file, 'r') as file:
            users = json.load(file)
        
        user = users.get(email)

        if user is None:
            return None

        is_admin = True if user.get('position') == Position.HR else False
        new_user_schema = UserSchemaAdd(
            is_admin=is_admin,
            is_verified=True,
            **user
        )
        new_user_dict = new_user_schema.model_dump()
        new_user = await self.user_repo.add(**new_user_dict)
        return new_user
        

    async def add_user(self, user: UserSchemaAdd):
        user_dict = user.model_dump()
        user = await self.user_repo.add(data=user_dict)
        return user

    async def get_or_create_user_by_email(self, email: str):
        user = await self.user_repo.get_one_by_fields(email=email)
        if user is not None:
            return user

        user = await self.check_users_file(email=email)
        return user

    async def get_unverified_users(self):
        unverified_users = await self.user_repo.get_all_by_fields(is_verified=False)
        return unverified_users

    async def get_user_by_id(self, user_id: int):
        user = await self.user_repo.get_by_id(id=user_id)
        return user

    async def get_users(self):
        user = await self.user_repo.get_all()
        return user

    async def get_user_orders(self, user_id: int):
        user = await self.user_repo.get_user_with_related(user_id=user_id)

        if user.orders:
            return sorted(user.orders, key=lambda obj: obj.created_at, reverse=True)
        else:
            return []

    async def get_user_benefits(self, user_id: int):
        user = await self.user_repo.get_user_with_related(user_id=user_id)

        if user.orders is None:
            return []

        user_benefits = []
        sorted_orders = sorted(user.orders, key=lambda obj: obj.created_at, reverse=True)
        for order in sorted_orders:
            if order.status == Status.APPROVED:
                user_benefits.append(order.benefit)

        return user_benefits

    async def verify_user_by_id(self, user_id: int, verified_data: UserSchemaUpdate, background_tasks: BackgroundTasks):
        verified_data_dict = verified_data.model_dump(exclude_unset=True)
        verified_data_dict.update({'is_verified': True})
        verified_user = await self.user_repo.update_by_id(id=user_id, new_data=verified_data_dict)

        if verified_user is not None:
            background_tasks.add_task(
                self.email_client.send_email,
                recipient_list=[verified_user.email],
                subject='Вход в аккаунт Кафетерий льгот UDV',
                text=(
                    f'Здравствуйте, {verified_user.first_name}!\n\n'
                    f'Ваш аккаунт был подтвержден, и теперь вы можете войти в него по почте {verified_user.email}'
                ),
                html=(
                    f'<b>Здравствуйте, {verified_user.first_name}!</b><br><br>'
                    f'Ваш аккаунт был подтвержден, и теперь вы можете войти в него по почте {verified_user.email}'
                ),
            )

        return verified_user

    async def update_user_by_id(self, user_id: int, new_data: UserSchemaUpdate):
        new_data_dict = new_data.model_dump(exclude_unset=True)
        updated_user = await self.user_repo.update_by_id(id=user_id, new_data=new_data_dict)
        return updated_user

    async def delete_user_by_id(self, user_id: int):
        await self.user_repo.delete_by_id(id=user_id)
