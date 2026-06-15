"""Skill: проверка миграций Django."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def run(context: dict[str, Any]) -> dict[str, Any]:
    root = Path(context.get("project_root", "."))
    migrations = []

    for app in ("catalog", "orders", "accounts"):
        mig_dir = root / "apps" / app / "migrations"
        if mig_dir.exists():
            files = [f.name for f in mig_dir.glob("*.py") if f.name != "__init__.py"]
            migrations.append({"app": app, "files": files})

    return {
        "status": "success",
        "migrations": migrations,
        "commands": ["python manage.py makemigrations", "python manage.py migrate"],
    }
