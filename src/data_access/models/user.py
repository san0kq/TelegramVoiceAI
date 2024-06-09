from __future__ import annotations

from typing import Optional

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy import BIGINT, Boolean, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin, TableNameMixin


users_values = Table(
    'users_values',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('value_id', ForeignKey('values.id'), primary_key=True),
)

class User(Base, TimestampMixin, TableNameMixin):

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    username: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    fullname: Mapped[str] = mapped_column(String(128), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, server_default=true())

    values: Mapped[list[Value]] = relationship(
        secondary=users_values, back_populates='users'
    )

    def __repr__(self):
        return f'<User {self.id} {self.username} {self.fullname}>'


class Value(Base, TimestampMixin, TableNameMixin):

    name: Mapped[Optional[str]] = mapped_column(String(128), unique=True)

    users: Mapped[list[User]] = relationship(
        secondary=users_values, back_populates='values'
    )

    def __repr__(self):
        return f'<{self.name}>'
