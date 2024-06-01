import uuid

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column


class MixinID:
    id: Mapped[uuid.UUID] = mapped_column(  # noqa A003
        UUID(as_uuid=True),
        server_default=func.gen_random_uuid(),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
