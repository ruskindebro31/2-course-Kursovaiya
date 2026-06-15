"""Skill: pytest для Candels backend."""

from __future__ import annotations

from typing import Any


def run(context: dict[str, Any]) -> dict[str, Any]:
    tests = [
        "test_category_list_api",
        "test_product_detail_by_slug",
        "test_jwt_login_and_refresh",
        "test_create_order_clears_cart",
        "test_order_status_permissions",
        "test_product_404_invalid_slug",
    ]
    return {
        "status": "success",
        "framework": "pytest-django",
        "command": "python -m pytest apps/ -v",
        "tests": tests,
        "coverage_target": 70,
    }
