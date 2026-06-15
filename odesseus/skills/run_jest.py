"""Skill: Jest для React frontend."""

from __future__ import annotations

from typing import Any


def run(context: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "success",
        "framework": "jest + @testing-library/react",
        "command": "cd frontend && npm test -- --watchAll=false",
        "tests": [
            "ProductList renders products",
            "CartPage updates quantity",
            "CheckoutForm validates fields",
            "LoginPage stores JWT in localStorage",
            "OrderStatusBadge shows websocket update",
        ],
    }
