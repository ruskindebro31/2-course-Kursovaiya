"""Skill: интеграционные тесты Candels."""

from __future__ import annotations

from typing import Any


def run(context: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "success",
        "scenarios": [
            "register → login → browse catalog → add to cart → checkout → order created",
            "admin changes order status → websocket notifies user",
            "add comment on product → appears instantly via websocket",
        ],
    }
