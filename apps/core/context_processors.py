import re

from django.conf import settings


def _phone_tel_href(phone: str) -> str:
    if not phone or not str(phone).strip():
        return ""
    digits = re.sub(r"\D", "", phone)
    if not digits:
        return ""
    if digits.startswith("8") and len(digits) >= 10:
        digits = "7" + digits[1:]
    return f"tel:+{digits}"


def shop_contacts(request):
    phone = (getattr(settings, "SHOP_PHONE", "") or "").strip()
    return {
        "shop_phone": phone,
        "shop_phone_tel": _phone_tel_href(phone),
        "shop_instagram_url": (getattr(settings, "SHOP_INSTAGRAM_URL", "") or "").strip(),
        "shop_telegram_url": (getattr(settings, "SHOP_TELEGRAM_URL", "") or "").strip(),
        "shop_whatsapp_url": (getattr(settings, "SHOP_WHATSAPP_URL", "") or "").strip(),
    }
