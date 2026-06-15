"""Skill: React Query кэш и оптимистичные обновления."""

from __future__ import annotations

from typing import Any


def run(context: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "success",
        "queries": [
            {"key": ["products"], "staleTime": 60000, "pagination": True},
            {"key": ["product", "slug"], "staleTime": 30000},
            {"key": ["cart"], "staleTime": 0},
            {"key": ["orders"], "staleTime": 10000},
            {"key": ["favorites"], "optimisticUpdate": True},
        ],
        "optimistic_patterns": [
            "addToFavorites — мгновенный UI, rollback при ошибке",
            "addComment — показ до ответа сервера",
            "updateCartQuantity — локальное обновление счётчика",
        ],
    }
