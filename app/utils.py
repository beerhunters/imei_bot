# utils.py
def validate_imei(imei: str) -> bool:
    return len(imei) == 15 and imei.isdigit()
