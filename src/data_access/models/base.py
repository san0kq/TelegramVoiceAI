from datetime import datetime

from sqlalchemy import BIGINT
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.functions import func


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(
        BIGINT, primary_key=True, autoincrement=True
    )



class TableNameMixin:
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, onupdate=func.now(), server_default=func.now())
