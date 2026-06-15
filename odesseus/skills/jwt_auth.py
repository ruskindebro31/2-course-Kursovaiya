"""Skill: JWT auth для Candels."""

from __future__ import annotations

from typing import Any


def run(context: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "success",
        "auth_scheme": "JWT Bearer",
        "endpoints": [
            {"method": "POST", "path": "/api/auth/register/"},
            {"method": "POST", "path": "/api/auth/login/"},
            {"method": "POST", "path": "/api/auth/token/refresh/"},
            {"method": "GET", "path": "/api/auth/profile/"},
            {"method": "PUT", "path": "/api/auth/profile/"},
        ],
        "settings": {
            "ACCESS_TOKEN_LIFETIME": "30 min",
            "REFRESH_TOKEN_LIFETIME": "1 day",
            "ROTATE_REFRESH_TOKENS": True,
            "AUTH_HEADER_TYPES": ("Bearer",),
        },
        "packages": ["djangorestframework-simplejwt", "django-cors-headers"],
    }
