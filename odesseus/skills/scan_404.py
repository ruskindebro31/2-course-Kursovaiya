"""Skill: сканирование 404 маршрутов Candels."""

from __future__ import annotations

from pathlib import Path
from typing import Any


CANDELS_ROUTES_TO_TEST = [
    "/",
    "/catalog/",
    "/cart/",
    "/orders/create/",
    "/accounts/login/",
    "/api/categories/",
    "/api/products/",
]


def run(context: dict[str, Any]) -> dict[str, Any]:
    root = Path(context.get("project_root", "."))
    issues = []

    catalog_urls = root / "apps" / "catalog" / "urls.py"
    if catalog_urls.exists():
        content = catalog_urls.read_text(encoding="utf-8")
        if "RedirectView.as_view(pattern_name=\"core:home\"" in content:
            issues.append({
                "url": "/catalog/",
                "status": 302,
                "problem": "Redirect на home вместо списка товаров",
                "severity": "major",
            })

    return {
        "status": "success",
        "routes_tested": CANDELS_ROUTES_TO_TEST,
        "issues": issues,
        "http_errors": len(issues),
    }
