from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.s3_client import S3Client
from app.internal.models import Benefit, BenefitContent, Option, User
from app.internal.repositories import BenefitRepository, BenefitContentRepository, OptionRepository, CategoryRepository, UserRepository
from app.internal.schemas import (
    BenefitSchema,
    BenefitType,
    BenefitSchemaAdd,
    BenefitSchemaUpdate,
    BenefitSchemaRel,
    EXPERIENCE_MAP,
    GroupedBenefitSchema,
    OptionSchema,
    Status,
)

from config import settings


class BenefitService:
    def __init__(
        self, 
        benefit_repo: BenefitRepository,
        benefit_content_repo: BenefitContentRepository,
        option_repo: OptionRepository,
        category_repo: CategoryRepository,
        user_repo: UserRepository,
        s3_client: S3Client,
        session: AsyncSession,
    ):
        self.benefit_repo: BenefitRepository = benefit_repo(session)
        self.benefit_content_repo: BenefitContentRepository = benefit_content_repo(session)
        self.option_repo: OptionRepository = option_repo(session)
        self.category_repo: CategoryRepository = category_repo(session)
        self.user_repo: UserRepository = user_repo(session)
        self.s3_client: S3Client = s3_client()
        self.session = session

    def is_enough_experience(self, user: User, required_experience: str):
        now = datetime.now(ZoneInfo(settings.TIMEZONE)).replace(tzinfo=None)
        user_experience = now.date() - user.work_start_date
        required = EXPERIENCE_MAP[required_experience].get('timedelta')

        return user_experience >= required

    def get_option_condition(self, option: Option, required_experience: str):
        message_base = f'Вариант «{option.title}» доступен сотрудникам со стажем от'
        return f'{message_base} {EXPERIENCE_MAP[required_experience].get('aliases')[0]}'

    async def get_benefits_by_availability(self, user: User, benefits: list[Benefit], available: bool = True):
        result_benefits = []
        for benefit in benefits:
            if benefit.childs_required and not user.has_children:
                if available:
                    continue
                else:
                    result_benefits.append(benefit)

            elif benefit.required_experience:
                if not self.is_enough_experience(user=user, required_experience=benefit.required_experience):
                    if available:
                        continue
                    else:
                        result_benefits.append(benefit)
            
            if available:
                result_benefits.append(benefit)

        return result_benefits

    async def add_benefit(self, benefit: BenefitSchemaAdd):
        async with self.session.begin():
            benefit_dict = benefit.model_dump(exclude={'content', 'options'})
            benefit_obj = Benefit(**benefit_dict)
            self.session.add(benefit_obj)

            await self.session.flush()

            content_dict = benefit.content.model_dump()
            content_dict.update(benefit_id=benefit_obj.id)
            content_obj = BenefitContent(**content_dict)
            self.session.add(content_obj)

            if benefit.options:
                for option in benefit.options:
                    option_dict = option.model_dump()
                    option_dict.update(benefit_id=benefit_obj.id)
                    option_obj = Option(**option_dict)
                    self.session.add(option_obj)

            await self.session.refresh(benefit_obj)

        return benefit_obj

    async def get_benefit_by_id(self, benefit_id: int, user_id: int):
        benefit = await self.benefit_repo.get_benefit_with_rel(benefit_id=benefit_id)
        options = benefit.options

        if options:
            benefit_dict = BenefitSchemaRel.model_validate(benefit).model_dump(exclude={'options'})
            user = await self.user_repo.get_by_id(id=user_id)

            updated_options = []
            for option in options:
                option_schema = OptionSchema.model_validate(option)
                if option.required_experience:
                    if not self.is_enough_experience(user=user, required_experience=option.required_experience):
                        option_schema.required_condition = self.get_option_condition(
                            option=option,
                            required_experience=option.required_experience
                        )
                        
                updated_options.append(option_schema)

            benefit_schema = BenefitSchemaRel(
                **benefit_dict,
                options=updated_options
            )

            return benefit_schema

        return benefit

    async def get_benefits(self):
        benefits = await self.benefit_repo.get_all()
        return benefits

    async def get_grouped_benefits(self, user_id: int, benefit_type: BenefitType):
        categories = await self.category_repo.get_categories_with_benefits()
        user = await self.user_repo.get_user_with_benefits(user_id=user_id)

        grouped_benefits = []
        for category in categories:
            match benefit_type:
                case BenefitType.AVAILABLE:
                    available_benefits = await self.get_benefits_by_availability(user=user, benefits=category.benefits, available=True)
                    category_benefits = GroupedBenefitSchema(
                        category_id=category.id,
                        category_title=category.title,
                        benefits=available_benefits,
                    )
                    grouped_benefits.append(category_benefits)
                case BenefitType.ACTIVE:
                    user_benefit_ids = []
                    for order in user.orders:
                        if order.status == Status.APPROVED:
                            user_benefit_ids.append(order.benefit.id)

                    user_benefits = []
                    for benefit in category.benefits:
                        if benefit.id in user_benefit_ids:
                            user_benefits.append(benefit)

                    category_benefits = GroupedBenefitSchema(
                        category_id=category.id,
                        category_title=category.title,
                        benefits=user_benefits,
                    )
                    grouped_benefits.append(category_benefits)
                case BenefitType.UNAVAILABLE:
                    unavailable_benefits = await self.get_benefits_by_availability(user=user, benefits=category.benefits, available=False)
                    category_benefits = GroupedBenefitSchema(
                        category_id=category.id,
                        category_title=category.title,
                        benefits=unavailable_benefits,
                    )
                    grouped_benefits.append(category_benefits)
                case _:
                    pass

        return grouped_benefits

    async def get_category_benefits_by_id(self, user_id: int, category_id: int, benefit_type: BenefitType):
        category = await self.category_repo.get_category_with_benefits_by_id(category_id=category_id)
        user = await self.user_repo.get_user_with_benefits(user_id=user_id)

        match benefit_type:
            case BenefitType.AVAILABLE:
                available_benefits = await self.get_benefits_by_availability(user=user, benefits=category.benefits, available=True)
                grouped_benefits = GroupedBenefitSchema(
                    category_id=category.id,
                    category_title=category.title,
                    benefits=available_benefits,
                )
            case BenefitType.ACTIVE:
                user_benefit_ids = []
                for order in user.orders:
                    if order.status == Status.APPROVED:
                        user_benefit_ids.append(order.benefit.id)

                user_benefits = []
                for benefit in category.benefits:
                    if benefit.id in user_benefit_ids:
                        user_benefits.append(benefit)

                grouped_benefits = GroupedBenefitSchema(
                    category_id=category.id,
                    category_title=category.title,
                    benefits=user_benefits,
                )
            case BenefitType.UNAVAILABLE:
                unavailable_benefits = await self.get_benefits_by_availability(user=user, benefits=category.benefits, available=False)
                grouped_benefits = GroupedBenefitSchema(
                    category_id=category.id,
                    category_title=category.title,
                    benefits=unavailable_benefits,
                )
            case _:
                grouped_benefits = GroupedBenefitSchema(
                    category_id=category.id,
                    category_title=category.title,
                    benefits=[],
                )

        return grouped_benefits

    async def update_benefit_by_id(self, benefit_id: int, new_data: BenefitSchemaUpdate):
        new_benefit_data = new_data.model_dump(exclude_unset=True, exclude={'content', 'options'})
        if new_benefit_data:
            await self.benefit_repo.update_by_id(id=benefit_id, new_data=new_benefit_data)
        
        if new_data.content:
            benefit = await self.benefit_repo.get_benefit_with_rel(benefit_id=benefit_id)
            new_content_data = new_data.content.model_dump(exclude_unset=True)
            await self.benefit_content_repo.update_by_id(id=benefit.content.id, new_data=new_content_data)

        if new_data.options:
            for option in new_data.options:
                option_id = option.id
                new_option_data = option.model_dump(exclude_unset=True, exclude={'id'})
                await self.option_repo.update_by_id(id=option_id, new_data=new_option_data)

        updated_benefit = await self.benefit_repo.get_benefit_with_rel(benefit_id=benefit_id)
        return updated_benefit

    async def update_benefit_picture(self, benefit_id: int, picture: UploadFile):
        benefit = await self.benefit_repo.get_by_id(id=benefit_id)

        file_url = await self.s3_client.upload(file=picture, path=f'benefits/{benefit_id}/')
        updated_benefit = await self.benefit_repo.update_by_id(id=benefit_id, new_data={'picture': file_url})

        return updated_benefit

    async def delete_benefit_by_id(self, benefit_id: int):
        await self.benefit_repo.delete_by_id(id=benefit_id)
