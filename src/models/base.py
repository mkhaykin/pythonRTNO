from typing import TypeVar

from sqlalchemy import event
from sqlalchemy.orm import DeclarativeBase, configure_mappers

from .mixin_id import MixinID
from .mixin_ts import MixinTimeStamp


class Base(DeclarativeBase):
    pass


class BaseModel(Base, MixinID, MixinTimeStamp):
    __abstract__ = True

    @classmethod
    def __declare_last__(cls) -> None:
        super().__declare_last__()


TBaseModel = TypeVar("TBaseModel", bound=BaseModel)


@event.listens_for(Base.metadata, "before_create")
def _configure_mappers(*args, **kwargs) -> None:  # noqa: ANN002, ANN003, U100
    configure_mappers()
