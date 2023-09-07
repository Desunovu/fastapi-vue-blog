from datetime import datetime
from enum import Enum

from pydantic import EmailStr, Field, BaseModel

from ...core.security.models import UserBase
from ...core.security.roles import RolesEnum
from ...utils.extended_document import ExtendedDocument


class UserDocument(ExtendedDocument, UserBase):
    username: str
    email: EmailStr
    role: RolesEnum | None = None
    disabled: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    password_hash: str | None = Field(default=None, exclude=True)

    class Settings:
        name = "users"


class UpdateUserRequest(BaseModel):
    """Модель для обновления информации о пользователе"""

    email: str


class UsersResponse(BaseModel):
    """Модель ответа списком пользователей"""

    users: list[UserDocument]


class UserResponse(BaseModel):
    """Модель ответа с одним пользователем"""

    user: UserDocument


class UsersSortField(str, Enum):
    """Поля по которым проводится сортировка"""

    username = "username"
    created_at = "created_at"
