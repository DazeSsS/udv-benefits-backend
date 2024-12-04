from enum import Enum
from datetime import datetime

from sqlalchemy import DateTime, desc, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from config import settings

from app.internal.orders.domain.schemas import Status


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[Status] = mapped_column(String(50), server_default=Status.IN_WORK.value)
    benefit_id: Mapped[int] = mapped_column(ForeignKey('benefit.id', ondelete='CASCADE'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    option_id: Mapped[int] = mapped_column(ForeignKey('option.id', ondelete='SET NULL'), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text(f"TIMEZONE('{settings.TIMEZONE}', CURRENT_TIMESTAMP)")
    )
    activated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    ends_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    benefit: Mapped['Benefit'] = relationship(back_populates='orders')
    user: Mapped['User'] = relationship(back_populates='orders')
    option: Mapped['Option'] = relationship()
    comments: Mapped[list['Comment']] = relationship(back_populates='order', order_by='desc(Comment.created_at)')
