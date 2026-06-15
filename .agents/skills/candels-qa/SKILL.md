---
name: candels-qa
description: QA Candels — pytest, Jest, интеграция, WebSocket load test
version: 1.0.0
category: qa
tags: [pytest, jest, testing, candels]
status: published
confidence: 0.85
source: taught
---

## When to Use

Когда нужно протестировать Candels после изменений бэкенда или фронтенда по критериям траектории В.

## Procedure

1. Backend: `python -m pytest apps/ -v --tb=short`.
2. Проверить APITestCase: categories, products, JWT login/refresh, create order.
3. Тест: корзина очищается после POST `/api/orders/`.
4. Тест: 404 на несуществующий product slug.
5. Frontend: `cd frontend && npm test -- --watchAll=false`.
6. Jest: ProductList, CartPage, CheckoutForm, LoginPage.
7. Integration: register → login → catalog → cart → checkout → order.
8. WebSocket: подключение к `ws/orders/1/`, получение status_changed.
9. Сформировать отчёт: passed/failed, coverage %, список багов.

## Pitfalls

- Перед тестами: `python manage.py migrate` и loaddata demo_catalog.json.
- Сервер должен быть запущен для integration-тестов.

## Verification

- pytest exit code 0.
- jest exit code 0.
- coverage ≥ 70% (цель траектории В).
