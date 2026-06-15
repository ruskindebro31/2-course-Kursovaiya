"""Skill: DRF API для Candels (catalog, orders)."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def run(context: dict[str, Any]) -> dict[str, Any]:
    root = Path(context.get("project_root", "."))

    endpoints = [
        {"method": "GET", "path": "/api/categories/", "view": "CategoryViewSet"},
        {"method": "GET", "path": "/api/products/", "view": "ProductViewSet"},
        {"method": "GET", "path": "/api/products/{slug}/", "view": "ProductViewSet"},
        {"method": "POST", "path": "/api/orders/", "view": "OrderViewSet"},
        {"method": "GET", "path": "/api/orders/", "view": "OrderViewSet"},
        {"method": "GET", "path": "/api/orders/{id}/", "view": "OrderViewSet"},
        {"method": "PATCH", "path": "/api/orders/{id}/status/", "view": "OrderViewSet"},
        {"method": "GET", "path": "/api/cart/", "view": "CartView"},
        {"method": "POST", "path": "/api/cart/add/", "view": "CartView"},
        {"method": "DELETE", "path": "/api/cart/clear/", "view": "CartView"},
    ]

    models_found = []
    for app in ("catalog", "orders", "accounts"):
        models_file = root / "apps" / app / "models.py"
        if models_file.exists():
            models_found.append(str(models_file))

    return {
        "status": "success",
        "trajectory": "V",
        "endpoints": endpoints,
        "models_files": models_found,
        "serializers_needed": ["CategorySerializer", "ProductSerializer", "OrderSerializer"],
        "permissions": ["AllowAny", "IsAuthenticated", "IsAdminUser"],
    }
