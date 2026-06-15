# Спецификация REST API

Базовый URL: `http://127.0.0.1:8000/api/`  
Swagger UI: `http://127.0.0.1:8000/api/docs/`

Аутентификация: `Authorization: Bearer <access_token>`

---

## Аутентификация

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/auth/register/` | Регистрация пользователя |
| POST | `/auth/login/` | Получение access + refresh токенов |
| POST | `/auth/token/refresh/` | Обновление access-токена |
| GET/PATCH | `/auth/profile/` | Профиль текущего пользователя |
| POST | `/token/verify/` | Проверка токена |

### Регистрация (POST /auth/register/)

```json
{
  "username": "user1",
  "email": "user@example.com",
  "first_name": "Имя",
  "last_name": "Фамилия",
  "password": "securepass123",
  "password_confirm": "securepass123"
}
```

### Вход (POST /auth/login/)

```json
{
  "email": "user@example.com",
  "password": "securepass123"
}
```

Ответ: `{ "access": "...", "refresh": "..." }`

---

## Категории

| Метод | Endpoint | Доступ |
|-------|----------|--------|
| GET | `/categories/` | Публичный |
| GET | `/categories/{id}/` | Публичный |

---

## Свечи (Candles)

| Метод | Endpoint | Доступ |
|-------|----------|--------|
| GET | `/candles/` | Публичный (только опубликованные) |
| GET | `/candles/{id}/` | Публичный |
| GET | `/candles/mine/` | Авторизованный (свои свечи) |
| POST | `/candles/` | Авторизованный |
| PUT/PATCH | `/candles/{id}/` | Автор (IsAuthorOrReadOnly) |
| DELETE | `/candles/{id}/` | Автор |

Параметры списка: `?search=`, `?category=`, `?ordering=`, пагинация `?page=`.

---

## Отзывы

| Метод | Endpoint | Доступ |
|-------|----------|--------|
| GET | `/reviews/?candle={id}` | Публичный |
| POST | `/reviews/` | Авторизованный |
| DELETE | `/reviews/{id}/` | Автор отзыва |

---

## Избранное

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/favorites/` | Список избранного |
| POST | `/favorites/toggle/` | Добавить/убрать `{ "candle": id }` |

---

## Корзина

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/carts/` | Корзина пользователя |
| POST | `/carts/add_item/` | Добавить товар |
| POST | `/carts/remove_item/` | Удалить позицию |

---

## Заказы

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/orders/` | История заказов |
| POST | `/orders/` | Оформление заказа из корзины |

---

## Уведомления

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/notifications/` | Список уведомлений |
| PATCH | `/notifications/{id}/` | Отметить прочитанным |

---

## WebSocket

| URL | Назначение |
|-----|------------|
| `ws://host/ws/notifications/{user_id}/` | Уведомления пользователя |
| `ws://host/ws/reviews/{candle_id}/` | Новые отзывы на свечу |
| `ws://host/ws/chat/{chat_id}/` | Сообщения чата |
