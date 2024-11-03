from enum import Enum
from datetime import date

from app.schema import BaseSchema
from app.internal.benefits.db.models import Period
from app.internal.categories.domain.schemas import CategorySchema


class BenefitType(str, Enum):
    AVAILABLE = 'available'
    ACTIVE = 'active'
    UNAVAILABLE = 'unavailable'


class BenefitSchemaAdd(BaseSchema):
    title: str
    description: str
    price: int
    period: Period
    instructions: str
    category_id: int
    is_cancellable: bool


class BenefitSchemaUpdate(BaseSchema):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    period: Period | None = None
    instructions: str | None = None
    category_id: int | None = None
    is_cancellable: bool | None = None


class BenefitSchema(BenefitSchemaAdd):
    id: int
    created_at: date


class BenefitSchemaRel(BenefitSchema):
    category: CategorySchema


class GroupedBenefitSchema(BaseSchema):
    category_id: int
    category_title: str
    benefits: list[BenefitSchema]
