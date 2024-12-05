from __future__ import annotations

from app.schema import BaseSchema

from app.internal.benefits.domain.schemas import BenefitSchema
from app.internal.categories.domain.schemas import CategorySchema


class StatisticsSchema(BaseSchema):
    active_benefits: int
    total_benefits: int
    total_users: int
    popular_benefit: BenefitSchema | None
    category_statistics: list[CategoryStatistics]


class CategoryStatistics(BaseSchema):
    category: CategorySchema
    active_benefits: int
