# api.py
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import settings

router = APIRouter()


class IMEIRequest(BaseModel):
    imei: str
    token: str


# Функция для проверки корректности IMEI
def validate_imei(imei: str) -> bool:
    # IMEI должен быть длиной 15 символов и содержать только цифры
    return len(imei) == 15 and imei.isdigit()


# Функция для проверки токена
def check_token(token: str):
    if token != settings.API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid API token")


# Эндпоинт для проверки IMEI
@router.post("/api/check-imei")
async def check_imei(request: IMEIRequest):
    # Проверка токена
    check_token(request.token)

    # Проверка корректности IMEI
    if not validate_imei(request.imei):
        raise HTTPException(status_code=400, detail="Invalid IMEI format")

    url = "https://api.imeicheck.net/v1/checks"
    payload = {"deviceId": request.imei, "serviceId": 12}
    headers = {
        "Authorization": f"Bearer {settings.API_TOKEN}",
        "Accept-Language": "en",
        "Content-Type": "application/json",
    }

    # Отправляем запрос в API imeicheck
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)

        # Проверка успешности ответа
        if response.status_code not in [200, 201]:
            raise HTTPException(
                status_code=500, detail="IMEI check service unavailable"
            )

        # Возвращаем ответ в формате JSON
        response_data = response.json()

        # Если в ответе есть предупреждение, выводим его
        if "!!! WARNING !!!" in response_data:
            warning_message = response_data["!!! WARNING !!!"]
            return {
                "status": "warning",
                "message": warning_message,
                "data": response_data,
            }

        return response_data

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=500, detail=f"Error during request to imeicheck API: {str(e)}"
        )
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail="Error with the response from imeicheck",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
