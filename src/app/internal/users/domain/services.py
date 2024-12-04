import os
import json

from fastapi import BackgroundTasks, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.email_client import EmailClient
from app.s3_client import S3Client
from app.internal.repositories import CommentRepository, UserRepository
from app.internal.schemas import OrderSchemaBenefit, Position, Status, UserSchemaAdd, UserSchemaUpdate

from config import settings


class UserService:
    def __init__(
        self,
        comment_repo: CommentRepository,
        user_repo: UserRepository,
        email_client: EmailClient,
        s3_client: S3Client,
        session: AsyncSession,
    ):
        self.comment_repo: CommentRepository = comment_repo(session)
        self.user_repo: UserRepository = user_repo(session)
        self.email_client: EmailClient = email_client()
        self.s3_client: S3Client = s3_client()
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
        new_user = await self.user_repo.add(data=new_user_dict)
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
        unverified_users = await self.user_repo.get_unverified_users()
        return unverified_users

    async def get_user_by_id(self, user_id: int):
        user = await self.user_repo.get_by_id(id=user_id)
        return user

    async def get_users(self):
        users = await self.user_repo.get_all_users()
        return users

    async def get_user_orders(self, user_id: int):
        user = await self.user_repo.get_user_with_related(user_id=user_id)
        orders = user.orders
        
        result_orders = []
        for order in orders:
            comments_count = await self.comment_repo.get_unread_comments_count(
                order_id=order.id, user_id=user_id
            )

            order_benefit = OrderSchemaBenefit.model_validate(order)
            order_benefit.unread_comments = comments_count

            result_orders.append(order_benefit)

        return result_orders

    async def get_user_benefits(self, user_id: int):
        user = await self.user_repo.get_user_with_related(user_id=user_id)

        if user.orders is None:
            return []

        user_benefits = []
        orders = user.orders
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

    async def update_user_photo(self, user_id: int, photo: UploadFile):
        user = await self.user_repo.get_by_id(id=user_id)

        file_url = await self.s3_client.upload(file=photo, path=f'users/{user_id}/')
        updated_user = await self.user_repo.update_by_id(id=user_id, new_data={'profile_photo': file_url})

        return updated_user

    async def delete_user_by_id(self, user_id: int):
        await self.user_repo.delete_by_id(id=user_id)
