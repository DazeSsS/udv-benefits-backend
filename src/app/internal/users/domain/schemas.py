from enum import Enum
from datetime import date
from pydantic import BaseModel, EmailStr


class PositionEnum(str, Enum):
    HR = 'hr'
    BACKEND = 'backend'
    FRONTEND = 'frontend'
    TESTER = 'tester'
    MANAGER = 'manager'


class UserSchemaAdd(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: str
    birth_date: date
    phone: str
    has_children: bool = False
    # TODO profile_photo
    work_start_date: date | None = None
    work_end_date: date | None = None
    position: PositionEnum | None = None
    department: str | None = None


class UserSchema(UserSchemaAdd):
    id: int
    is_admin: bool
    is_verified: bool
    coins: int


class UserInfoSchema(BaseModel):
    id: int
    is_admin: bool
