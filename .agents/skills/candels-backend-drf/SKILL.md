---
name: candels-backend-drf
description: Бэкенд Candels — DRF API, JWT, Django Channels (траектория В)
version: 1.0.0
category: dev
tags: [django, drf, jwt, channels, candels]
status: published
confidence: 0.9
source: taught
---

## When to Use

Когда нужно реализовать или доработать бэкенд интернет-магазина Candels по траектории В из МУ_КП_ТРПО: REST API, JWT, WebSocket для статусов заказов.

## Procedure

1. Работать только в `C:\Users\vacba\Desktop\Candels` (Docker: `/workspace/candels`).
2. Установить пакеты: `django`, `djangorestframework`, `djangorestframework-simplejwt`, `django-cors-headers`, `channels`, `pillow`, `python-dotenv`.
3. Настроить `config/settings.py`: REST_FRAMEWORK, SIMPLE_JWT, CORS, CHANNEL_LAYERS, ASGI.
4. Создать API-маршруты: `/api/categories/`, `/api/products/`, `/api/orders/`, `/api/auth/*`.
5. Реализовать ViewSet + Serializer для `Category`, `Product`, `Order`, `OrderItem` в apps/catalog и apps/orders.
6. JWT: register, login, token/refresh, profile в apps/accounts.
7. WebSocket consumer для `ws/orders/<id>/` — real-time смена статуса заказа.
8. Permissions: guest (read), user (CRUD своих), admin (full).
9. Запустить: `python manage.py makemigrations && python manage.py migrate`.
10. Проверить: `python manage.py runserver` и GET `/api/products/`.

## Pitfalls

- Не ломать текущие Django Templates — API добавляется параллельно через `/api/`.
- CORS: добавить `http://localhost:3000` в CORS_ALLOWED_ORIGINS.
- После POST `/api/orders/` корзина должна очищаться (баг из PROJECT_PROBLEMS.md).

## Verification

- 10+ REST эндпоинтов отвечают 200/201.
- JWT login возвращает access + refresh.
- WebSocket отправляет событие при смене status заказа.
- `python -m pytest apps/ -v` проходит.
