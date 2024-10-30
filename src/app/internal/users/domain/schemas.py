from enum import Enum
from datetime import date
from pydantic import BaseModel, EmailStr


class PositionEnum(str, Enum):
    hr = 'HR'
    backend = 'Backend разработчик'
    frontend = 'Frontend разработчик'
    tester = 'Тестировщик'
    manager = 'Менеджер'


class UserSchemaAdd(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: str
    birth_date: date
    has_children: bool
    # TODO profile_photo
    work_start_date: date
    work_end_date: date | None = None
    position: PositionEnum
    department: str


class UserSchema(UserSchemaAdd):
    id: int
    is_admin: bool
    is_verified: bool
    coins: int
