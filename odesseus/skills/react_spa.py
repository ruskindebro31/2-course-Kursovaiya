"""Skill: React SPA структура для Candels."""

from __future__ import annotations

from typing import Any


def run(context: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "success",
        "frontend_dir": "frontend/",
        "routes": [
            {"/": "HomePage"},
            {"/catalog": "ProductListPage"},
            {"/catalog/:slug": "ProductDetailPage"},
            {"/cart": "CartPage"},
            {"/checkout": "CheckoutPage"},
            {"/orders": "OrderListPage"},
            {"/orders/:id": "OrderDetailPage"},
            {"/login": "LoginPage"},
            {"/register": "RegisterPage"},
            {"/profile": "ProfilePage"},
        ],
        "components": [
            "ProductCard", "ProductList", "CartItem", "CheckoutForm",
            "OrderStatusBadge", "CommentThread", "FavoriteButton",
        ],
    }
