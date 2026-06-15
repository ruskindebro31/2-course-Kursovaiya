"""Skill: чеклист развёртывания траектории В."""

from __future__ import annotations

from typing import Any


def run(context: dict[str, Any]) -> dict[str, Any]:
    checklist = [
        {"item": "DRF + JWT настроены", "done": False},
        {"item": "React SPA собирается (npm run build)", "done": False},
        {"item": "WebSocket работает через Channels", "done": False},
        {"item": "docker-compose up поднимает все сервисы", "done": False},
        {"item": "OpenAPI документация /api/schema/", "done": False},
        {"item": "Git-стatistics в README.md", "done": False},
    ]
    return {
        "status": "success",
        "checklist": checklist,
        "completed": sum(1 for c in checklist if c["done"]),
        "total": len(checklist),
    }
