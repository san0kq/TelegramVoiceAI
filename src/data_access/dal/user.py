from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from logging import getLogger

from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload


from data_access import db_session
from data_access.models import User, Value
from data_access.dto import UserDTO
from data_access.exceptions import (
    UserAlreadyExistsError,
    AddUserError,
    GetUserError,
    GetValueError,
    ValueAlreadyExistsError,
    AddValueError
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import async_scoped_session, AsyncSession
    from data_access.dto import ValueDTO


logger = getLogger(__name__)


class UserDAL:
    def __init__(self, db_session: async_scoped_session[AsyncSession] = db_session) -> None:
        self._db_session = db_session
    
    async def create_user(self, data: UserDTO) -> Optional[User]:
        try:
            async with self._db_session.begin():
                user = User(
                    id=data.user_id,
                    username=data.username,
                    fullname=data.fullname,
                    active=data.active
                )
                self._db_session.add(user)
                await self._db_session.commit()

                logger.info(
                    'New user added. User ID: %s', data.user_id
                )
                return user
            
        except IntegrityError as err:
            logger.info(
                'Duplicate User "%s": %s', data.user_id, err
            )
            await self._db_session.rollback()
            raise UserAlreadyExistsError(
                'User already exists. User ID: %s', data.user_id
            )
        except Exception as err:
            logger.error('Add new user ERROR: %s', err)
            await self._db_session.rollback()
            raise AddUserError(
                f'Add new user failed. User ID: {data.user_id}'
            )
    
    async def create_value(self, data: ValueDTO) -> Optional[Value]:
        try:
            async with self._db_session.begin():
                value = Value(
                    name=data.value.lower()
                )
                self._db_session.add(value)
                logger.info(
                    'New value added. Value: %s', data.value.lower()
                )
                return value
            
        except IntegrityError as err:
            logger.error(
                'Duplicate Value "%s" ERROR: %s', data.value.lower(), err
            )
            await self._db_session.rollback()
            raise ValueAlreadyExistsError(
                'Value already exists. Value: %s', data.value.lower()
            )
        except Exception as err:
            logger.error('Create new value ERROR: %s', err)
            await self._db_session.rollback()
            raise AddValueError(
                f'Create new value failed. Value: {data.value.lower()}'
            )

    async def get_user(self, data: UserDTO) -> Optional[User]:
        try:
            async with self._db_session.begin():
                stmt = select(User).where(User.id == data.user_id)
                result = await self._db_session.execute(stmt)
                user = result.one_or_none()
                return user
        except Exception as err:
            logger.error('Get user ERROR: %s', err)
            raise GetUserError(
                f'Get user failed. User ID: {data.user_id}'
            )

    async def get_value(self, data: ValueDTO) -> Optional[Value]:
        try:
            async with self._db_session.begin():
                stmt = select(Value).where(Value.name == data.value.lower())
                result = await self._db_session.execute(stmt)
                value = result.one_or_none()
                return value
        except Exception as err:
            logger.error('Get value ERROR: %s', err)
            raise GetValueError(
                f'Get value failed. Value: {data.value.lower()}'
            )

    async def add_value(self, data: ValueDTO) -> None:
        user_stmt = select(User).where(User.id == data.user_id).options(selectinload(User.values))
        value_stmt = select(Value).where(Value.name == data.value.lower())

        try:
            async with self._db_session() as session:
                async with session.begin():
                    user_result = await session.execute(user_stmt)
                    value_result = await session.execute(value_stmt)
                    user = user_result.scalar_one_or_none()
                    value = value_result.scalar_one_or_none()

                    if not value:
                        value = Value(name=data.value.lower())
                        session.add(value)

                    user.values.append(value)

                    await session.commit()
        
        except Exception as err:
            logger.error('Add value ERROR: %s', err)
            raise GetValueError(
                f'Add value failed. Value: {data.value.lower()}'
            )
