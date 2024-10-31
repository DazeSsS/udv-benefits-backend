from enum import Enum
from datetime import date

from sqlalchemy import Date, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from config import settings


class Period(Enum):
    ONE_YEAR = 'one_year'
    ONE_MONTH = 'one_month'
    THREE_MONTHS = 'three_months'


class Benefit(Base):
    __tablename__ = 'benefit'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[str]
    price: Mapped[int]
    period: Mapped[Period] = mapped_column(String(25))
    instructions: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id', ondelete='RESTRICT'))
    is_cancellable: Mapped[bool]
    сreated_at: Mapped[date] = mapped_column(
        Date,
        server_default=text(f"DATE(TIMEZONE('{settings.TIMEZONE}', CURRENT_TIMESTAMP))")
    )

    # TODO: add variations of benefit
    # TODO: add conditions for purchasing a benefit
    category: Mapped['Category'] = relationship(back_populates='benefits')
