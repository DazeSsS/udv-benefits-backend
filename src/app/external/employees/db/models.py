from enum import Enum
from datetime import date

from sqlalchemy import Boolean, Date, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Position(Enum):
    hr = 'HR'
    backend = 'Backend разработчик'
    frontend = 'Frontend разработчик'
    tester = 'Тестировщик'
    manager = 'Менеджер'


class Employee(Base):
    __tablename__ = 'employee'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    middle_name: Mapped[str] = mapped_column(String(50), nullable=True)
    birth_date: Mapped[date] = mapped_column(Date)
    has_children: Mapped[bool] = mapped_column(Boolean, server_default='false')
    work_start_date: Mapped[date] = mapped_column(Date)
    work_end_date: Mapped[date] = mapped_column(Date, nullable=True)
    position: Mapped[Position] = mapped_column(String(50))
    department: Mapped[str] = mapped_column(String(50))