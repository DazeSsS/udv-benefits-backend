from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    icon: Mapped[str] = mapped_column(nullable=True)

    benefits: Mapped[list['Benefit']] = relationship(back_populates='category')
