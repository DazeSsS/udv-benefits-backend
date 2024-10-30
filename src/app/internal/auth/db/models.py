from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from config import settings


class Token(Base):
    __tablename__ = 'token'

    jti: Mapped[str] = mapped_column(String(255), primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text(f"TIMEZONE('{settings.TIMEZONE}', CURRENT_TIMESTAMP)")
    )
    revoked: Mapped[bool] = mapped_column(server_default='false')

    user: Mapped['User'] = relationship(back_populates='tokens')
