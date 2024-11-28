from enum import Enum
from datetime import datetime

from pydantic import computed_field

from app.schema import BaseSchema
from app.internal.benefits.domain.schemas import BenefitSchema, BenefitSchemaRel
from app.internal.comments.domain.schemas import CommentSchemaRel
from app.internal.users.domain.schemas import UserSchema


class Status(str, Enum):
    APPROVED = 'approved'
    REJECTED = 'rejected'
    IN_WORK = 'in_work'
    INACTIVE = 'inactive'


class OrderSchemaAdd(BaseSchema):
    benefit_id: int


class OrderSchemaUpdate(OrderSchemaAdd):
    status: Status | None = None
    benefit_id: int | None = None
    user_id: int | None = None
    activated_at: datetime | None = None
    ends_at: datetime | None = None


class OrderSchema(OrderSchemaAdd):
    id: int
    status: Status
    user_id: int
    created_at: datetime
    activated_at: datetime | None = None
    ends_at: datetime | None = None


class OrderSchemaBenefit(OrderSchema):
    benefit: BenefitSchema
    unread_comments: int = 0


class OrderSchemaUser(OrderSchemaBenefit):
    user: UserSchema


class OrderSchemaDetail(OrderSchema):
    benefit: BenefitSchemaRel
    comments: list[CommentSchemaRel]
