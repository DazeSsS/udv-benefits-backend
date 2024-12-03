from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from config import settings


class Comment(Base):
    __tablename__ = 'comment'

    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column(String(2000))
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id', ondelete='CASCADE'))
    sender_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    attachment_id: Mapped[int] = mapped_column(ForeignKey('attachment.id', ondelete='SET NULL'), nullable=True)
    is_read: Mapped[bool] = mapped_column(server_default='false')
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text(f"TIMEZONE('{settings.TIMEZONE}', CURRENT_TIMESTAMP)")
    )

    attachment: Mapped['Attachment'] = relationship(lazy='joined')
    order: Mapped['Order'] = relationship(back_populates='comments')
    sender: Mapped['User'] = relationship()
