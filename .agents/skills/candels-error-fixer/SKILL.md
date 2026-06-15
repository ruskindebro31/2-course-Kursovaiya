---
name: candels-error-fixer
description: Исправление 404, CORS, static, известных багов Candels
version: 1.0.0
category: fix
tags: [404, cors, routes, candels]
status: published
confidence: 0.9
source: taught
---

## When to Use

Когда появляются независимые ошибки: 404, битые ссылки, CORS, static/media, редиректы catalog → home, корзина не очищается.

## Procedure

1. Прочитать `PROJECT_PROBLEMS.md` — список известных багов.
2. Сканировать URL: `/`, `/catalog/`, `/cart/`, `/orders/create/`, `/api/products/`.
3. Проверить `apps/catalog/urls.py` — RedirectView на home заменить на ProductListView.
4. Проверить `config/urls.py` — добавить `path('api/', include(...))` если отсутствует.
5. CORS: corsheaders в INSTALLED_APPS, CorsMiddleware первым, origins localhost:3000.
6. Static/media: STATIC_URL, MEDIA_URL, collectstatic, demo images в media/products/.
7. После заказа: в OrderCreateView вызвать `cart.clear()`.
8. React: добавить catch-all route `*` → NotFoundPage.
9. Записать неисправленное обратно в PROJECT_PROBLEMS.md.

## Pitfalls

- Не удалять рабочие Django Templates при добавлении API.
- Проверять reverse() name= совпадает с templates.

## Verification

- GET `/catalog/` возвращает список, не redirect на home.
- POST order → cart пустая.
- Нет CORS error в консоли браузера.
- scan_404: 0 critical issues.
