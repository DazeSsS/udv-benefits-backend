from __future__ import annotations

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
    ONE_MONTH = 'one_month'
    TWO_MONTHS = 'two_months'
    THREE_MONTHS = 'three_months'
    SIX_MONTHS = 'six_months'
    ONE_YEAR = 'one_year'
    TWO_YEARS = 'two_years'


EXPERIENCE_MAP = {
    Experience.ONE_MONTH: {
        'timedelta': timedelta(days=30),
        'aliases': ['1-го месяца']
    },
    Experience.THREE_MONTHS: {
        'timedelta': timedelta(days=90),
        'aliases': ['3-х месяцев']
    },
    Experience.SIX_MONTHS: {
        'timedelta': timedelta(days=180),
        'aliases': ['6-ти месяцев']
    },
    Experience.NINE_MONTHS: {
        'timedelta': timedelta(days=270),
        'aliases': ['9-ти месяцев']
    },
    Experience.ONE_YEAR: {
        'timedelta': timedelta(days=365),
        'aliases': ['1-го года']
    },
    Experience.TWO_YEARS: {
        'timedelta': timedelta(days=730),
        'aliases': ['2-х лет']
    },
    Experience.THREE_YEARS: {
        'timedelta': timedelta(days=1095),
        'aliases': ['3-х лет']
    },
    Experience.FOUR_YEARS: {
        'timedelta': timedelta(days=1460),
        'aliases': ['4-х лет']
    },
    Experience.FIVE_YEARS: {
        'timedelta': timedelta(days=1825),
        'aliases': ['5-ти лет']
    },
}


PERIOD_MAP = {
    Period.ONE_MONTH: timedelta(days=30),
    Period.TWO_MONTHS: timedelta(days=60),
    Period.THREE_MONTHS: timedelta(days=90),
    Period.THREE_MONTHS: timedelta(days=180),
    Period.ONE_YEAR: timedelta(days=365),
    Period.TWO_YEARS: timedelta(days=730),
}


class BenefitSchemaAdd(BaseSchema):
    title: str
    provider: str
    description: str
    picture: str | None = None
    price: int
    required_experience: Experience | None = None
    childs_required: bool = False
    category_id: int
    is_active: bool = True
    content: BenefitContentSchemaAdd
    options: list[OptionSchemaAdd] | None = None


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
    required_experience: Experience | None = None
    childs_required: bool | None = None
    category_id: int | None = None
    is_active: bool | None = None
    content: BenefitContentSchemaUpdate | None = None
    options: list[OptionSchemaUpdate] | None = None


class BenefitContentSchemaUpdate(BaseSchema):
    instructions: str | None = None
    period: Period | None = None
    is_cancellable: bool | None = None


class OptionSchemaUpdate(BaseSchema):
    id: int
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


class OptionSchema(OptionSchemaAdd):
    id: int
    required_condition: str | None = None


class BenefitSchemaRel(BenefitSchema):
    content: BenefitContentSchemaAdd
    options: list[OptionSchema] | None


class GroupedBenefitSchema(BaseSchema):
    category_id: int
    category_title: str
    benefits: list[BenefitSchema]
