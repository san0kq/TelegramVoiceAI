from typing import Optional

from data_access.dto import UserDTO
from data_access.dal import UserDAL
from data_access.exceptions import (
    UserAlreadyExistsError,
    AddUserError,
    GetUserError
)


async def create_user(
        user_id: int,
        username: Optional[str] = None,
        fullname: Optional[str] = None
) -> bool:
    data = UserDTO(
        user_id=user_id,
        username=username,
        fullname=fullname
    )
    dal = UserDAL()

    try:
        await dal.create_user(data=data)
        return True

    except (UserAlreadyExistsError, AddUserError, GetUserError):
        return False
