from enum import Enum
from datetime import datetime, timedelta

from app.schema import BaseSchema
from app.internal.categories.domain.schemas import CategorySchema


class BenefitType(str, Enum):
    AVAILABLE = 'available'
    ACTIVE = 'active'
    UNAVAILABLE = 'unavailable'


class Experience(str, Enum):
    ONE_MONTH = 'one_month'
    THREE_MONTHS = 'three_months'
    SIX_MONTHS = 'six_months'
    NINE_MONTHS = 'nine_months'
    ONE_YEAR = 'one_year'
    TWO_YEARS = 'two_years'
    THREE_YEARS = 'three_years'
    FOUR_YEARS = 'four_years'
    FIVE_YEARS = 'five_years'


class Period(str, Enum):
    ONE_YEAR = 'one_year'
    ONE_MONTH = 'one_month'
    THREE_MONTHS = 'three_months'


EXPERIENCE_MAP = {
    Experience.ONE_MONTH: timedelta(days=30),
    Experience.THREE_MONTHS: timedelta(days=90),
    Experience.SIX_MONTHS: timedelta(days=180),
    Experience.NINE_MONTHS: timedelta(days=270),
    Experience.ONE_YEAR: timedelta(days=365),
    Experience.TWO_YEARS: timedelta(days=730),
    Experience.THREE_YEARS: timedelta(days=1095),
    Experience.FIVE_YEARS: timedelta(days=1825)
}


PERIOD_MAP = {
    Period.ONE_YEAR: timedelta(days=365),
    Period.ONE_MONTH: timedelta(days=30),
    Period.THREE_MONTHS: timedelta(days=90)
}


class BenefitSchemaAdd(BaseSchema):
    title: str
    provider: str
    description: str
    price: int
    required_experience: Experience | None = None
    childs_required: bool = False
    category_id: int
    is_active: bool = True
    content: 'BenefitContentSchemaAdd'
    options: list['OptionSchemaAdd'] | None = None


class BenefitContentSchemaAdd(BaseSchema):
    instructions: str
    period: Period | None = None
    is_cancellable: bool


class OptionSchemaAdd(BaseSchema):
    title: str
    description: str
    required_experience: Experience | None = None


class BenefitSchemaUpdate(BaseSchema):
    title: str | None = None
    provider: str | None = None
    description: str | None = None
    price: int | None = None
    period: Period | None = None
    instructions: str | None = None
    category_id: int | None = None
    is_cancellable: bool | None = None


class BenefitContentSchemaUpdate(BaseSchema):
    instructions: str | None = None
    period: Period | None = None
    is_cancellable: bool | None = None


class OptionSchemaUpdate(BaseSchema):
    title: str | None = None
    description: str | None = None
    required_experience: Experience | None = None


class BenefitSchema(BaseSchema):
    id: int
    title: str
    provider: str
    description: str
    picture: str | None
    price: int
    required_experience: Experience | None
    childs_required: bool
    category_id: int
    is_active: bool
    created_at: datetime
    category: CategorySchema


class BenefitSchemaRel(BenefitSchema):
    content: 'BenefitContentSchemaAdd'
    options: list['OptionSchemaAdd'] | None


class GroupedBenefitSchema(BaseSchema):
    category_id: int
    category_title: str
    benefits: list['BenefitSchema']
