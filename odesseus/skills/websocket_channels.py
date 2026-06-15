"""Skill: Django Channels WebSocket для статусов заказов."""

from __future__ import annotations

from typing import Any


def run(context: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "success",
        "websocket_routes": [
            {"path": "ws/orders/<int:order_id>/", "consumer": "OrderStatusConsumer"},
            {"path": "ws/products/<slug:slug>/comments/", "consumer": "CommentConsumer"},
        ],
        "channel_layer": "channels.layers.InMemoryChannelLayer",
        "production_layer": "channels_redis.core.RedisChannelLayer",
        "events": ["order_status_changed", "new_comment", "favorite_updated"],
        "packages": ["channels", "channels-redis"],
    }
