from datetime import datetime

from app.schema import BaseSchema
from app.internal.orders.db.models import Status
from app.internal.benefits.domain.schemas import BenefitSchemaRel


class OrderSchemaAdd(BaseSchema):
    benefit_id: int
    user_id: int


class OrderSchemaUpdate(OrderSchemaAdd):
    status: Status | None = None
    benefit_id: int | None = None
    user_id: int | None = None
    activated_at: datetime | None = None
    ends_at: datetime | None = None


class OrderSchema(OrderSchemaAdd):
    id: int
    status: Status
    created_at: datetime
    activated_at: datetime | None = None
    ends_at: datetime | None = None


class OrderSchemaRel(OrderSchema):
    benefit: BenefitSchemaRel
