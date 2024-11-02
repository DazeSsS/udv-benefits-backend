from enum import Enum
from datetime import date
from pydantic import BaseModel, ConfigDict


class PeriodEnum(str, Enum):
    ONE_YEAR = 'one_year'
    ONE_MONTH = 'one_month'
    THREE_MONTHS = 'three_months'


class BenefitSchemaAdd(BaseModel):
    title: str
    description: str
    price: int
    period: PeriodEnum
    instructions: str
    category_id: int
    is_cancellable: bool


class BenefitSchemaUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    instructions: str | None = None
    category_id: int | None = None
    period: PeriodEnum | None = None
    is_cancellable: bool | None = None


class BenefitSchema(BenefitSchemaAdd):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: date


class GroupedBenefitSchema(BaseModel):
    category_id: int
    category_title: str
    benefits: list['BenefitSchema']
