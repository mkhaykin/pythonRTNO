import uuid
from enum import Enum, unique

from sqlalchemy import UUID, BigInteger, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM as pgEnum
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import BaseModel
from src.models.mixin_id import MixinID
from src.models.mixin_ts import MixinTimeStamp


@unique
class DirectionEnum(Enum):
    IN = "in"
    OUT = "out"
    FORWARD = "forward"


class Message(BaseModel, MixinID, MixinTimeStamp):
    __tablename__ = "messages"

    original_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        index=True,
        nullable=False,
    )

    parent_id: Mapped[uuid.UUID] = mapped_column(  # A003
        UUID(as_uuid=True),
        ForeignKey("messages.id"),
        unique=False,
        index=False,  # TODO: think
        nullable=True,
    )

    original_parent_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=False,
        index=True,
        nullable=True,
    )

    source: Mapped[str] = mapped_column(
        String,
        unique=False,
        index=False,
        nullable=False,
        default="tg",
        server_default="tg",
    )

    direction: Mapped[str] = mapped_column(
        pgEnum(DirectionEnum, name="directionenum"),
        unique=False,
        index=False,
        nullable=False,
        default="IN",
        server_default="IN",
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

    __table_args__ = (UniqueConstraint("original_id", "source", name="uc_message"),)

    def __repr__(self) -> str:
        return f"{self.user_name}: '{self.text[:20] + '...'}')"
