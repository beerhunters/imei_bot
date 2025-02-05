# main.py
import asyncio
import uvicorn
from fastapi import FastAPI
from app.bot import start_bot
from app.api import router as api_router
from app.config import settings
from app.database import async_main
from app.rq import add_allowed_users_to_db

app = FastAPI()
app.include_router(api_router)


async def main():
    # Инициализация базы данных и добавление разрешённых пользователей
    await async_main()
    await add_allowed_users_to_db(settings.allowed_user_ids)

    # Запускаем бота в фоновом режиме
    bot_task = asyncio.create_task(start_bot())

    # Запуск сервера в другом таске
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)

    # Создаём таск для сервера
    server_task = asyncio.create_task(server.serve())

    # Ожидаем завершения всех задач
    await bot_task
    await server_task


if __name__ == "__main__":
    asyncio.run(main())
