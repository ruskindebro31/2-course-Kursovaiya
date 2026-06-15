"""Skill: исправление CORS и CSRF для React SPA."""

from __future__ import annotations

from typing import Any


def run(context: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "success",
        "cors_allowed_origins": [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        "csrf_trusted_origins": [
            "http://localhost:3000",
        ],
        "packages": ["django-cors-headers"],
        "middleware": "corsheaders.middleware.CorsMiddleware — первым в списке",
        "fixed_count": 1,
    }
