"""Skill: известные баги Candels из PROJECT_PROBLEMS.md."""

from __future__ import annotations

from typing import Any


KNOWN_FIXES = [
    {
        "id": "cart_not_cleared_after_order",
        "description": "Корзина не очищается после оформления заказа",
        "fix": "В OrderCreateView после успешного POST вызвать cart.clear()",
        "file": "apps/orders/views.py",
        "severity": "major",
    },
    {
        "id": "catalog_redirects_to_home",
        "description": "catalog/ и category/ редиректят на home",
        "fix": "Реализовать ProductListView и CategoryListView",
        "file": "apps/catalog/urls.py",
        "severity": "major",
    },
    {
        "id": "missing_order_status_ui",
        "description": "Пользователь не видит статус заказа",
        "fix": "OrderDetailPage + WebSocket OrderStatusConsumer",
        "file": "frontend/src/pages/OrderDetailPage.tsx",
        "severity": "major",
    },
]


def run(context: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "success",
        "known_fixes": KNOWN_FIXES,
        "fixed_count": 0,
        "source": "PROJECT_PROBLEMS.md",
    }
