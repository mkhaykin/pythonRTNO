from aiogram.types import User


def user_name(user: User | None) -> str:
    if user is None:
        return "none"
    else:
        return user.username or user.first_name or user.full_name or str(user.id)
