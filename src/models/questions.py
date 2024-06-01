import uuid

from sqlalchemy import BigInteger, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import BaseModel
from src.models.mixin_ts import MixinTimeStamp


class Question(BaseModel, MixinTimeStamp):
    __tablename__ = "questions"

    id: Mapped[uuid.UUID] = mapped_column(  # noqa A003
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
    )

    message_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        index=True,
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=False,
        index=True,
        nullable=False,
    )

    user_name: Mapped[str] = mapped_column(
        String,
        unique=False,
        index=True,
        nullable=False,
    )

    text: Mapped[str] = mapped_column(
        String,
        unique=False,
        index=False,
        nullable=False,
        default="",
        server_default="",
    )

    def __repr__(self) -> str:
        return f"{self.user_name}: '{self.text[:20] + '...'}')"
