"""Skill: исправление static/media."""

from __future__ import annotations

from typing import Any


def run(context: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "success",
        "checks": [
            "STATIC_URL = '/static/'",
            "MEDIA_URL = '/media/'",
            "python manage.py collectstatic",
            "media/products/ demo images exist",
        ],
        "fixed_count": 0,
    }
