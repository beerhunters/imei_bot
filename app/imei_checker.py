import httpx
from app.config import settings
import json


async def check_imei_api(device_id: str) -> dict:
    url = "https://api.imeicheck.net/v1/checks"

    payload = {"deviceId": device_id, "serviceId": 12}

    headers = {
        "Authorization": f"Bearer {settings.API_TOKEN}",
        "Accept-Language": "en",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        # Отправляем POST запрос
        response = await client.post(url, headers=headers, json=payload)

    if response.status_code not in [200, 201]:
        raise Exception(f"Ошибка: {response.status_code} - {response.text}")

    # Получаем данные ответа
    response_data = response.json()

    # Проверяем на наличие тестового предупреждения
    if "!!! WARNING !!!" in response_data:
        warning_message = response_data["!!! WARNING !!!"]
        response_data["test_mode_warning"] = (
            "Вы используете тестовые данные в песочнице. Это не реальные данные."
        )

        # Можно вывести предупреждение в логах, если нужно
        # print(warning_message)

        # Отправляем только предупреждающее сообщение
        # await message.answer(
        #     f"Внимание: {warning_message}\nТестовый режим активен. Эти данные не реальные."
        # )
        print(warning_message)
    else:
        # Если нет тестового предупреждения, просто отправляем данные
        # await message.answer(json.dumps(response_data, ensure_ascii=False))
        print(json.dumps(response_data, ensure_ascii=False))
    return response_data
    # return json.dumps(response_data, ensure_ascii=False)


async def format_imei_response(response_data: dict) -> str:
    # Формируем сообщение
    if "!!! WARNING !!!" in response_data:
        warning_message = response_data["!!! WARNING !!!"]
        test_mode_warning = response_data["test_mode_warning"]

        # Структурируем данные
        formatted_message = f"<b>Внимание!</b>\n\n"
        formatted_message += f"<b>Тестовый режим:</b> {test_mode_warning}\n"
        formatted_message += f"<b>Предупреждение:</b> {warning_message}\n\n"

        # Информация об устройстве
        properties = response_data.get("properties", {})
        formatted_message += (
            f"<b>Устройство:</b> {properties.get('deviceName', 'Неизвестно')}\n"
        )
        formatted_message += f"<b>IMEI:</b> {properties.get('imei', 'Неизвестно')}\n"
        formatted_message += f"<b>MEID:</b> {properties.get('meid', 'Неизвестно')}\n"
        formatted_message += (
            f"<b>Серийный номер:</b> {properties.get('serial', 'Неизвестно')}\n"
        )
        formatted_message += f"<b>Страна покупки:</b> {properties.get('purchaseCountry', 'Неизвестно')}\n"

        # Состояние устройства
        formatted_message += f"<b>Черный список GSMA:</b> {'Да' if properties.get('gsmaBlacklisted', False) else 'Нет'}\n"
        formatted_message += (
            f"<b>Заменено:</b> {'Да' if properties.get('replaced', False) else 'Нет'}\n"
        )
        formatted_message += f"<b>FMI:</b> {'Включено' if properties.get('fmiOn', False) else 'Отключено'}\n"
        formatted_message += f"<b>Статус блокировки T-Mobile:</b> {properties.get('usaBlockStatus', 'Неизвестно')}\n"

        # Дополнительная информация
        formatted_message += f"\n<b>Сервис:</b> {response_data.get('service', {}).get('title', 'Неизвестно')}\n"
        formatted_message += (
            f"<b>Статус запроса:</b> {response_data.get('status', 'Неизвестно')}\n"
        )
        formatted_message += (
            f"<b>Сумма:</b> {response_data.get('amount', 'Неизвестно')} USD\n"
        )

        # Добавим изображение устройства
        device_image = properties.get("image", "")
        if device_image:
            formatted_message += f"<b>Изображение устройства:</b> <a href='{device_image}'>Смотреть</a>\n"

        # Возвращаем готовое сообщение
        return formatted_message

    return "Ошибка: Не удалось обработать данные."
