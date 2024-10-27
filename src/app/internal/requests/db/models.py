from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from config import settings


class Request(Base):
    __tablename__ = 'request'

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[str] = mapped_column(String(25))
    benefit_id: Mapped[int] = mapped_column(ForeignKey('benefit.id', ondelete='RESTRICT'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    сreated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text(f"TIMEZONE('{settings.TIMEZONE}', CURRENT_TIMESTAMP)")
    )

    benefit: Mapped['Benefit'] = relationship()
    user: Mapped['User'] = relationship(back_populates='requests')
    comments: Mapped[list['Comment']] = relationship(back_populates='request')
