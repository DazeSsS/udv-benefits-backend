from enum import Enum
from datetime import date, timedelta

from sqlalchemy import Date, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from config import settings


class Period(str, Enum):
    ONE_YEAR = 'one_year'
    ONE_MONTH = 'one_month'
    THREE_MONTHS = 'three_months'


PERIOD_MAP = {
    Period.ONE_YEAR: timedelta(days=365),
    Period.ONE_MONTH: timedelta(days=30),
    Period.THREE_MONTHS: timedelta(days=90)
}


class Benefit(Base):
    __tablename__ = 'benefit'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(256))
    description: Mapped[str]
    price: Mapped[int]
    period: Mapped[Period] = mapped_column(String(25), nullable=True)
    instructions: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id', ondelete='RESTRICT'))
    is_cancellable: Mapped[bool]
    created_at: Mapped[date] = mapped_column(
        Date,
        server_default=text(f"DATE(TIMEZONE('{settings.TIMEZONE}', CURRENT_TIMESTAMP))")
    )

    # TODO: add variations of benefit
    # TODO: add conditions for purchasing a benefit
    orders: Mapped[list['Order']] = relationship(back_populates='benefit')
    category: Mapped['Category'] = relationship(back_populates='benefits')
