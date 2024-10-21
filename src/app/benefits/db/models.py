from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Benefit(Base):
    __tablename__ = 'benefit'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1000))
    price: Mapped[int]
    period: Mapped[str] # TODO: change type of period field
    instructions: Mapped[str] = mapped_column(String(1000))
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id', ondelete='RESTRICT'))
    is_cancellable: Mapped[bool]

    # TODO: add conditions for purchasing a benefit
    category: Mapped['Category'] = relationship(back_populates='benefits')
