"""Skill: проверка Docker/docker-compose."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def run(context: dict[str, Any]) -> dict[str, Any]:
    root = Path(context.get("project_root", "."))
    required = ["docker-compose.yml", "Dockerfile", ".env.example"]
    missing = [f for f in required if not (root / f).exists()]

    return {
        "status": "success" if not missing else "warning",
        "missing_files": missing,
        "expected_services": ["django", "react", "postgres", "redis"],
        "channels_redis": "channels_redis.core.RedisChannelLayer for production",
    }
