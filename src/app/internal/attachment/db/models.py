from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Attachment(Base):
    __tablename__ = 'attachment'

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(nullable=False)
    file_url: Mapped[str] = mapped_column(nullable=False)
