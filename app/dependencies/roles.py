from collections.abc import Callable

from fastapi import Depends

from app.core.exceptions import ForbiddenException
from app.dependencies.auth import get_current_user
from app.models.user import User


def require_roles(*allowed_roles: str) -> Callable:
    async def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role.name not in allowed_roles:
            raise ForbiddenException()

        return current_user

    return role_checker