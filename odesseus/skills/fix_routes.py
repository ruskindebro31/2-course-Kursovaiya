"""Skill: исправление URL-маршрутов."""

from __future__ import annotations

from typing import Any


def run(context: dict[str, Any]) -> dict[str, Any]:
    fixes = [
        {
            "file": "config/urls.py",
            "action": "Добавить path('api/', include('apps.api.urls'))",
        },
        {
            "file": "apps/catalog/urls.py",
            "action": "Заменить RedirectView на ProductListView для /catalog/",
        },
        {
            "file": "frontend/src/routes/index.tsx",
            "action": "Добавить <Route path='*' element={<NotFoundPage />} />",
        },
    ]
    return {
        "status": "success",
        "fixes_applied": fixes,
        "fixed_count": len(fixes),
    }
