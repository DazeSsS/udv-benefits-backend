from enum import Enum
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from zoneinfo import ZoneInfo
from pydantic import EmailStr, computed_field

from app.schema import BaseSchema
from app.internal.users.db.models import Position

from config import settings


class WorkExperienceSchema(BaseSchema):
    years: int
    months: int


class UserSchemaAdd(BaseSchema):
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: str | None = None
    birth_date: date
    phone: str
    has_children: bool = False
    is_admin: bool | None = False
    is_verified: bool | None = False
    # TODO profile_photo
    work_start_date: date | None = None
    work_end_date: date | None = None
    position: Position | None = None
    department: str | None = None


class UserSchemaUpdate(BaseSchema):
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    birth_date: date | None = None
    phone: str | None = None
    has_children: bool | None = None
    is_admin: bool | None = None
    work_start_date: date | None = None
    work_end_date: date | None = None
    position: Position | None = None
    department: str | None = None
    balance: int | None = None


class UserSchema(UserSchemaAdd):
    id: int
    is_admin: bool
    is_verified: bool
    balance: int

    @computed_field
    def work_experience(self) -> WorkExperienceSchema | None:
        if self.work_start_date:
            end_date = (
                self.work_end_date
                if self.work_end_date
                else datetime.now(ZoneInfo(settings.TIMEZONE)).replace(tzinfo=None)
            )
            difference = relativedelta(end_date, self.work_start_date)
            years = difference.years
            months = difference.months

            return WorkExperienceSchema(years=years, months=months)


class UserInfoSchema(BaseSchema):
    id: int
    is_admin: bool
