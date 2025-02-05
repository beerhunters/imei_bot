# config.py
from pydantic_settings import BaseSettings

from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    API_TOKEN: str = os.getenv("API_TOKEN")
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    ALLOWED_USERS: str = os.getenv("ALLOWED_USERS", "")

    @property
    def allowed_user_ids(self):
        # Преобразуем строку в список целых чисел
        return [int(user_id) for user_id in self.ALLOWED_USERS.split(",") if user_id]

    class Config:
        env_file = ".env"


settings = Settings()
