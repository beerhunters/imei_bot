# api.py
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import settings

router = APIRouter()


class IMEIRequest(BaseModel):
    imei: str
    token: str


def validate_imei(imei: str) -> bool:
    return len(imei) == 15 and imei.isdigit()


def check_token(token: str):
    if token != settings.API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid API token")


@router.post("/api/check-imei")
async def check_imei(request: IMEIRequest):
    check_token(request.token)
    if not validate_imei(request.imei):
        raise HTTPException(status_code=400, detail="Invalid IMEI format")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://imeicheck.net/api/check/{request.imei}",
            headers={"Authorization": f"Bearer {settings.API_TOKEN}"},
        )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="IMEI check service unavailable")

    return response.json()
