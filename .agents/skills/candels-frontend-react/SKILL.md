---
name: candels-frontend-react
description: React SPA Candels — каталог, корзина, JWT, React Query, WebSocket
version: 1.0.0
category: dev
tags: [react, typescript, react-query, websocket, candels]
status: published
confidence: 0.9
source: taught
---

## When to Use

Когда нужно создать или доработать фронтенд Candels: React SPA с JWT, React Query и WebSocket-клиентом.

## Procedure

1. Создать или открыть папку `frontend/` в корне Candels.
2. Инициализировать React + TypeScript + Vite (или CRA).
3. Настроить React Router: `/`, `/catalog`, `/catalog/:slug`, `/cart`, `/checkout`, `/orders/:id`, `/login`, `/register`.
4. Axios instance с baseURL `http://127.0.0.1:8000/api` и interceptor для JWT refresh.
5. React Query: кэш products, cart, orders; staleTime 30–60 сек.
6. Оптимистичные обновления для избранного и комментариев.
7. useWebSocket хук для `ws://127.0.0.1:8000/ws/orders/{id}/`.
8. Компоненты: ProductList, ProductCard, CartPage, CheckoutForm, OrderStatusBadge.
9. Fallback: если WebSocket недоступен — polling GET `/api/orders/{id}/` каждые 10 сек.
10. Запуск: `npm run dev` на порту 3000.

## Pitfalls

- Токены хранить в localStorage, не в cookies (траектория В).
- Обрабатывать 401 → refresh token → retry request.
- Route `*` → NotFoundPage для 404 на клиенте.

## Verification

- SPA открывается на localhost:3000.
- Каталог загружается с API.
- Оформление заказа работает end-to-end.
- Статус заказа обновляется через WebSocket.
