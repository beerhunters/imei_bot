from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session
from app.models import User


def connection(some_func):
    async def wrapper(*args, **kwargs):
        # Подключение сессии, передаем в функцию
        async with async_session() as session:
            return await some_func(session, *args, **kwargs)

    return wrapper


# Применяем декоратор
@connection
async def is_user_allowed(session: AsyncSession, user_id: int) -> bool:
    # Используем сессию, переданную в аргумент
    result = await session.execute(
        select(User).filter(User.telegram_id == str(user_id))
    )
    user = result.scalars().first()
    return user is not None


@connection
async def add_allowed_users_to_db(session: AsyncSession, allowed_user_ids: list):
    # Проверяем, какие из разрешённых пользователей уже есть в базе
    for user_id in allowed_user_ids:
        # Проверяем, существует ли пользователь с таким ID
        result = await session.execute(
            select(User).filter(User.telegram_id == str(user_id))
        )
        user = result.scalars().first()

        if not user:
            # Если пользователь не найден, добавляем его в базу
            new_user = User(
                telegram_id=str(user_id)
            )  # или добавьте другие поля, если необходимо
            session.add(new_user)

    # Сохраняем изменения в базе
    await session.commit()
