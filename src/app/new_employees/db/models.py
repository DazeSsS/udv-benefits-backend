from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class NewEmployee(Base):
    __tablename__ = 'new_employee'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    admin_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'))

    admin: Mapped['User'] = relationship(back_populates='new_employees')
