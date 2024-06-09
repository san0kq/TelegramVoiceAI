from typing import Optional
from dataclasses import dataclass


@dataclass
class UserDTO:
    user_id: int
    username: Optional[str] = None
    fullname: Optional[str] = None
    active: bool = True


@dataclass
class ValueDTO:
    user_id: int
    value: str
