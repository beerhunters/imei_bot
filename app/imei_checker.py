# imei_checker.py
import ssl

import aiohttp
from app.config import settings


async def check_imei_api(imei: str) -> str:
    url = f"https://imeicheck.net/api/check/{imei}"
    headers = {"Authorization": f"Bearer {settings.API_TOKEN}"}

    # Создаем контекст SSL с отключенной проверкой сертификатов
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, ssl=ssl_context) as response:
            if response.status != 200:
                return "Ошибка сервиса проверки IMEI. Попробуйте позже."
            data = await response.json()
            return str(data)
