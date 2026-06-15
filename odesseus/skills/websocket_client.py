"""Skill: WebSocket клиент React."""

from __future__ import annotations

from typing import Any


def run(context: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "success",
        "hooks": ["useWebSocket", "useOrderStatus", "useCommentStream"],
        "endpoints": {
            "order_status": "ws://127.0.0.1:8000/ws/orders/{id}/",
            "comments": "ws://127.0.0.1:8000/ws/products/{slug}/comments/",
        },
        "fallback": "polling GET /api/orders/{id}/ every 10s if websocket fails",
    }
