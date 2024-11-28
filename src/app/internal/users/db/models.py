from enum import Enum
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from config import settings

from app.internal.users.domain.schemas import Position


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    middle_name: Mapped[str] = mapped_column(String(50), nullable=True)
    birth_date: Mapped[date] = mapped_column(Date)
    phone: Mapped[str] = mapped_column(String(15))
    is_admin: Mapped[bool] = mapped_column(Boolean, server_default='false')
    is_verified: Mapped[bool] = mapped_column(Boolean, server_default='false')
    has_children: Mapped[bool] = mapped_column(Boolean, server_default='false')
    # profile_photo
    work_start_date: Mapped[date] = mapped_column(Date, nullable=True)
    work_end_date: Mapped[date] = mapped_column(Date, nullable=True)
    legal_entity: Mapped[str] = mapped_column(String(128))
    position: Mapped[Position] = mapped_column(String(50), nullable=True)
    department: Mapped[str] = mapped_column(String(50), nullable=True)
    balance: Mapped[int] = mapped_column(Integer, server_default=f'{settings.BALANCE_DEFAULT}')
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text(f"TIMEZONE('{settings.TIMEZONE}', CURRENT_TIMESTAMP)")
    )
    
    orders: Mapped[list['Order']] = relationship(back_populates='user', order_by='desc(Order.created_at)')
    tokens: Mapped[list['Token']] = relationship(back_populates='user')
