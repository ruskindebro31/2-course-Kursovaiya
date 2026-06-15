"""Skill: code review для Candels."""

from __future__ import annotations

from typing import Any


def run(context: dict[str, Any]) -> dict[str, Any]:
    artifact = context.get("artifact_type", "unknown")
    issues = []

    if artifact == "backend":
        issues.append({"severity": "major", "message": "Проверить REST_FRAMEWORK и SIMPLE_JWT в settings.py"})
        issues.append({"severity": "minor", "message": "Добавить select_related для Product → Category"})

    if artifact == "frontend":
        issues.append({"severity": "minor", "message": "React.memo для ProductCard при большом каталоге"})

    approved = not any(i["severity"] == "critical" for i in issues)

    return {
        "status": "success",
        "artifact_type": artifact,
        "approved": approved,
        "issues": issues,
        "summary": f"Review {artifact}: {'OK' if approved else 'needs fixes'}",
    }
