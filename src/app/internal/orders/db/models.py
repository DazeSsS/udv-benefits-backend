from enum import Enum
from datetime import date

from sqlalchemy import Date, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from config import settings


class Status(Enum):
    APPROVED = 'approved'
    REJECTED = 'rejected'
    IN_WORK = 'in_work'
    INACTIVE = 'inactive'


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[Status] = mapped_column(String(50))
    benefit_id: Mapped[int] = mapped_column(ForeignKey('benefit.id', ondelete='RESTRICT'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    сreated_at: Mapped[date] = mapped_column(
        Date,
        server_default=text(f"DATE(TIMEZONE('{settings.TIMEZONE}', CURRENT_TIMESTAMP))")
    )
    activated_at: Mapped[date] = mapped_column(Date, nullable=True)
    ends_at: Mapped[date] = mapped_column(Date, nullable=True)

    benefit: Mapped['Benefit'] = relationship()
    user: Mapped['User'] = relationship(back_populates='orders')
    comments: Mapped[list['Comment']] = relationship(back_populates='order')
