from enum import Enum
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from config import settings

from app.internal.benefits.domain.schemas import Experience, Period


class Benefit(Base):
    __tablename__ = 'benefit'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(256))
    provider: Mapped[str] = mapped_column(String(256))
    description: Mapped[str] = mapped_column(String(2000))
    price: Mapped[int]
    required_experience: Mapped[Experience] = mapped_column(String(25), nullable=True)
    childs_required: Mapped[bool] = mapped_column(Boolean, server_default='false')
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id', ondelete='RESTRICT'))
    is_active: Mapped[bool] = mapped_column(Boolean, server_default='true')
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text(f"TIMEZONE('{settings.TIMEZONE}', CURRENT_TIMESTAMP)")
    )

    options: Mapped[list['Option']] = relationship(back_populates='benefit')
    orders: Mapped[list['Order']] = relationship(back_populates='benefit')
    category: Mapped['Category'] = relationship(back_populates='benefits', lazy='joined')
    content: Mapped['BenefitContent'] = relationship(back_populates='benefit')


class BenefitContent(Base):
    __tablename__ = 'benefit_content'

    id: Mapped[int] = mapped_column(primary_key=True)
    benefit_id: Mapped[int] = mapped_column(ForeignKey('benefit.id', ondelete='CASCADE'), unique=True, nullable=False)
    instructions: Mapped[str] = mapped_column(String(2000), nullable=True)
    period: Mapped[Period] = mapped_column(String(25), nullable=True)
    is_cancellable: Mapped[bool]

    benefit: Mapped['Benefit'] = relationship(back_populates='content')


class Option(Base):
    __tablename__ = 'option'

    id: Mapped[int] = mapped_column(primary_key=True)
    benefit_id: Mapped[int] = mapped_column(ForeignKey('benefit.id', ondelete='CASCADE'))
    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(String(2000))
    required_experience: Mapped[Experience] = mapped_column(String(25), nullable=True)

    benefit: Mapped['Benefit'] = relationship(back_populates='options')
