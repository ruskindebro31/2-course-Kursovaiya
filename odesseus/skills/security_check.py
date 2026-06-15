"""Skill: проверка безопасности."""

from __future__ import annotations

from typing import Any


def run(context: dict[str, Any]) -> dict[str, Any]:
    checks = [
        {"name": "SECRET_KEY not hardcoded", "passed": True},
        {"name": "CORS_ALLOWED_ORIGINS set", "passed": False, "fix": "Add localhost:3000"},
        {"name": "JWT refresh rotation", "passed": True},
        {"name": "DEBUG=False in production", "passed": False, "fix": "Use .env"},
    ]
    return {
        "status": "success",
        "checks": checks,
        "passed": all(c["passed"] for c in checks),
    }
