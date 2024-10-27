from enum import Enum
from datetime import date

from sqlalchemy import Boolean, Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from config import settings


class Position(Enum):
    hr = 'HR'
    backend = 'Backend разработчик'
    frontend = 'Frontend разработчик'
    tester = 'Тестировщик'
    manager = 'Менеджер'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    middle_name: Mapped[str] = mapped_column(String(50), nullable=True)
    birth_date: Mapped[date] = mapped_column(Date)
    is_admin: Mapped[bool] = mapped_column(Boolean, server_default='false')
    is_verified: Mapped[bool] = mapped_column(Boolean, server_default='false')
    has_children: Mapped[bool] = mapped_column(Boolean, server_default='false')
    # profile_photo
    work_start_date: Mapped[date] = mapped_column(Date)
    work_end_date: Mapped[date] = mapped_column(Date, nullable=True)
    position: Mapped[Position] = mapped_column(String(50))
    department: Mapped[str] = mapped_column(String(50))
    coins: Mapped[int] = mapped_column(Integer, server_default=f'{settings.COINS_DEFAULT}')
    
    requests: Mapped[list['Request']] = relationship(back_populates='user')
    new_employees: Mapped[list['NewEmployee']] = relationship(back_populates='admin')
