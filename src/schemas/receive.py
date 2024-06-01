from __future__ import annotations

import uuid

from aiogram.types import Message


class MsgIn(Message):
    db_id: uuid.UUID | None = None
