# WebSocket и real-time функции

## Технологии

- **Django Channels** — ASGI-слой для WebSocket.
- **InMemoryChannelLayer** (разработка) / **Redis Channel Layer** (продакшен).

## Маршруты (routing.py)

| WebSocket URL | Consumer | События |
|---------------|----------|---------|
| `ws/notifications/<user_id>/` | NotificationConsumer | новые уведомления пользователю |
| `ws/reviews/<candle_id>/` | ReviewConsumer | новый отзыв на странице свечи |
| `ws/chat/<chat_id>/` | ChatConsumer | сообщения в чате |

## Backend

При создании отзыва, заказа или уведомления сервер:
1. Сохраняет запись в БД.
2. Отправляет событие в группу Channel Layer (`group_send`).
3. Consumer рассылает JSON клиентам, подключённым к группе.

## Frontend

- `hooks/useNotifications.js` — подключение к `ws/notifications/{userId}/` при авторизации.
- `components/ReviewList.jsx` — подписка на `ws/reviews/{candleId}/`, обновление списка без перезагрузки.

## Оптимистичные обновления

**Избранное:** UI переключает состояние сразу; при ошибке API — откат.

**Отзывы:** новый отзыв добавляется в список локально; WebSocket синхронизирует у других клиентов.

## React Query кэширование

- `staleTime: 30_000` — каталог не перезапрашивается 30 секунд.
- `invalidateQueries` после мутаций (создание свечи, заказ).

## Запуск ASGI

```bash
cd backend
daphne candels.asgi:application
# или
uvicorn candels.asgi:application
```

Для разработки `runserver` с Channels также поддерживает WebSocket.
