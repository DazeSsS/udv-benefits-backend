from enum import Enum
from datetime import date
from pydantic import BaseModel, ConfigDict

from app.internal.benefits.db.models import Period


class BenefitSchemaAdd(BaseModel):
    title: str
    description: str
    price: int
    period: Period
    instructions: str
    category_id: int
    is_cancellable: bool


class BenefitSchemaUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    period: Period | None = None
    instructions: str | None = None
    category_id: int | None = None
    is_cancellable: bool | None = None


class BenefitSchema(BenefitSchemaAdd):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: date


class GroupedBenefitSchema(BaseModel):
    category_id: int
    category_title: str
    benefits: list['BenefitSchema']
