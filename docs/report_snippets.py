"""Встроенные фрагменты для build_full_report.py."""

USE_CASE = """```mermaid
flowchart LR
    subgraph Actors
        Guest((Гость))
        User((Пользователь))
        Author((Автор))
    end

    subgraph System["Candels"]
        UC1[Просмотр каталога]
        UC2[Регистрация]
        UC3[Вход]
        UC4[Профиль]
        UC5[Избранное]
        UC6[Корзина]
        UC7[Заказ]
        UC8[Отзыв]
        UC9[CRUD свечей]
        UC10[Уведомления RT]
    end

    Guest --> UC1
    Guest --> UC2
    Guest --> UC3
    User --> UC1
    User --> UC4
    User --> UC5
    User --> UC6
    User --> UC7
    User --> UC8
    User --> UC10
    Author --> UC9
    Author --> UC8
```

## Спецификации прецедентов

### UC-01 Просмотр каталога

| Поле | Значение |
|------|----------|
| Актор | Гость, Пользователь |
| Предусловие | Backend запущен |
| Основной поток | 1. Открыть /catalog 2. API GET /candles/ 3. Отобразить карточки |
| Постусловие | Список свечей на экране |

### UC-02 Регистрация

| Поле | Значение |
|------|----------|
| Актор | Гость |
| Основной поток | 1. Форма register 2. POST /auth/register/ 3. Redirect login |
| Альтернатива | Email занят → сообщение об ошибке |

### UC-03 JWT-вход

| Поле | Значение |
|------|----------|
| Актор | Пользователь |
| Основной поток | 1. POST /auth/login/ 2. Сохранить токены 3. Доступ к защищённым страницам |

### UC-09 CRUD своих свечей

| Поле | Значение |
|------|----------|
| Актор | Автор |
| Предусловие | JWT valid |
| Основной поток | Create/Update/Delete через /candles/ и /candles/mine/ |
| Ограничение | Только author == current user |

### UC-10 Real-time уведомления

| Поле | Значение |
|------|----------|
| Актор | Пользователь |
| Основной поток | 1. WebSocket connect 2. Событие на сервере 3. Push в UI |"""

DOMAIN_MODEL = """```mermaid
classDiagram
    class User {
        +username
        +email
        +password
        +register()
        +login()
    }

    class Profile {
        +avatar
        +bio
        +phone
        +update()
    }

    class Category {
        +name
        +slug
        +description
    }

    class Candle {
        +name
        +description
        +price
        +is_published
        +publish()
        +unpublish()
    }

    class Review {
        +rating
        +comment
        +create()
    }

    class Favorite {
        +toggle()
    }

    class Cart {
        +addItem()
        +removeItem()
        +clear()
    }

    class Order {
        +total_price
        +status
        +checkout()
    }

    class Notification {
        +message
        +is_read
        +markRead()
    }

    class Chat {
        +participants
    }

    class Message {
        +text
        +send()
    }

    User "1" --> "1" Profile
    User "1" --> "*" Candle : authors
    User "1" --> "1" Cart
    User "1" --> "*" Order
    User "1" --> "*" Review
    User "1" --> "*" Favorite
    User "1" --> "*" Notification
    Category "1" --> "*" Candle
    Candle "1" --> "*" Review
    Candle "1" --> "*" Favorite
    Cart "1" --> "*" CartItem
    Order "1" --> "*" OrderItem
    Chat "1" --> "*" Message
    User "*" --> "*" Chat
```

## Агрегаты

| Агрегат | Корневая сущность | Инварианты |
|---------|-------------------|------------|
| Каталог | Candle | цена > 0; категория обязательна |
| Заказ | Order | сумма = Σ позиций; статус из enum |
| Корзина | Cart | одна корзина на пользователя |
| Отзыв | Review | рейтинг 1–5; один отзыв на пару user+candle |"""

ARCHITECTURE = """## Общая схема

```mermaid
flowchart TB
    subgraph Client["Клиент (React SPA)"]
        Pages[Страницы / Router]
        RQ[TanStack Query]
        WS[WebSocket hooks]
        Store[Zustand cartStore]
    end

    subgraph Server["Сервер (Django)"]
        DRF[DRF ViewSets]
        JWT[SimpleJWT]
        CH[Channels Consumers]
        ORM[Django ORM]
    end

    DB[(SQLite / PostgreSQL)]
    Redis[(Redis — опционально)]

    Pages --> RQ
    Pages --> WS
    Pages --> Store
    RQ -->|HTTP REST| DRF
    WS -->|WebSocket| CH
    DRF --> JWT
    DRF --> ORM
    CH --> ORM
    ORM --> DB
    CH -.-> Redis
```

## Слои backend

| Слой | Компоненты |
|------|------------|
| Presentation | ViewSet, Serializer, Consumers |
| Business | permissions, signals, queryset filters |
| Data | Models, migrations |
| Infrastructure | settings, ASGI, routing |

## Слои frontend

| Слой | Компоненты |
|------|------------|
| UI | pages/, components/ |
| State | AuthContext, cartStore, React Query cache |
| API | api/client.js (Axios + interceptors) |
| Real-time | useNotifications, ReviewList WebSocket |

## Поток аутентификации

1. Пользователь вводит email/пароль → `POST /api/auth/login/`.
2. Сервер возвращает access (короткий) и refresh (длинный) токены.
3. Клиент сохраняет токены в localStorage.
4. Axios interceptor добавляет `Authorization: Bearer <access>`.
5. При 401 — запрос `POST /api/auth/token/refresh/`, повтор исходного запроса.

## Поток оформления заказа

1. Добавление в корзину → `POST /api/carts/add_item/`.
2. Просмотр корзины → `GET /api/carts/`.
3. Оформление → `POST /api/orders/` (создание Order + OrderItem, очистка корзины).
4. Уведомление автору → Notification + WebSocket push.

## Развёртывание

- **Разработка:** `runserver` (backend) + `npm run dev` (frontend, proxy на API).
- **Продакшен:** Gunicorn/Uvicorn + Nginx для статики SPA и проксирования API/WebSocket."""

JWT_AUTH_DESIGN = """## Выбор схемы

Для траектории В используется **stateless JWT** (библиотека `djangorestframework-simplejwt`):

- **Access token** — короткоживущий, передаётся в заголовке каждого запроса.
- **Refresh token** — долгоживущий, используется только для получения нового access.

## Endpoints

```
POST /api/auth/register/     → создание User + Profile
POST /api/auth/login/        → { access, refresh }
POST /api/auth/token/refresh/ → { access }
GET  /api/auth/profile/      → данные пользователя (требует access)
POST /api/token/verify/      → проверка валидности токена
```

## Настройки (settings.py)

- `REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES']`: `JWTAuthentication`
- `SIMPLE_JWT`: время жизни access/refresh, алгоритм HS256
- `AUTH_USER_MODEL = 'users.User'`

## Клиентская реализация (frontend/src/api/client.js)

1. При логине — сохранение `access` и `refresh` в `localStorage`.
2. Request interceptor — подстановка Bearer-токена.
3. Response interceptor — при 401 попытка refresh и повтор запроса.
4. При неудачном refresh — logout, редирект на `/login`.

## Безопасность

- Пароли хранятся как Django hash (PBKDF2).
- HTTPS в продакшене обязателен для защиты токенов.
- CORS настроен только для доверенных origin (localhost:5173).
- `token_blacklist` подключён для возможности инвалидации refresh-токенов.

## Диаграмма последовательности

```mermaid
sequenceDiagram
    participant U as Пользователь
    participant SPA as React SPA
    participant API as Django REST
    participant DB as БД

    U->>SPA: email + password
    SPA->>API: POST /auth/login/
    API->>DB: проверка credentials
    DB-->>API: User
    API-->>SPA: access + refresh
    SPA->>SPA: localStorage

    U->>SPA: запрос каталога
    SPA->>API: GET /candles/ + Bearer
    API-->>SPA: JSON данные

    Note over SPA,API: access истёк
    SPA->>API: POST /auth/token/refresh/
    API-->>SPA: новый access
    SPA->>API: повтор исходного запроса
```"""

ER_DIAGRAM = """```mermaid
erDiagram
    User ||--o| Profile : has
    User ||--o| Cart : owns
    User ||--o{ Candle : authors
    User ||--o{ Order : places
    User ||--o{ Review : writes
    User ||--o{ Favorite : has
    User ||--o{ Notification : receives
    User }o--o{ Chat : participates

    Category ||--o{ Candle : contains
    Candle ||--o{ Review : has
    Candle ||--o{ Favorite : in
    Candle ||--o{ CartItem : in
    Candle ||--o{ OrderItem : in

    Cart ||--o{ CartItem : contains
    Order ||--o{ OrderItem : contains
    Chat ||--o{ Message : contains
    User ||--o{ Message : sends

    User {
        int id PK
        string username
        string email UK
        string password
        datetime date_joined
    }

    Profile {
        int id PK
        int user_id FK
        string avatar
        text bio
        string phone
    }

    Category {
        int id PK
        string name UK
        string slug UK
        text description
        bool is_active
    }

    Candle {
        int id PK
        string name
        text description
        decimal price
        int category_id FK
        int author_id FK
        string image
        bool is_published
        datetime created_at
    }

    Review {
        int id PK
        int user_id FK
        int candle_id FK
        int rating
        text comment
        datetime created_at
    }

    Favorite {
        int id PK
        int user_id FK
        int candle_id FK
    }

    Cart {
        int id PK
        int user_id FK
        datetime created_at
    }

    CartItem {
        int id PK
        int cart_id FK
        int candle_id FK
        int quantity
    }

    Order {
        int id PK
        int user_id FK
        decimal total_price
        string status
        datetime created_at
    }

    OrderItem {
        int id PK
        int order_id FK
        int candle_id FK
        int quantity
        decimal price
    }

    Notification {
        int id PK
        int user_id FK
        text message
        bool is_read
        datetime created_at
    }

    Chat {
        int id PK
        datetime created_at
    }

    Message {
        int id PK
        int chat_id FK
        int sender_id FK
        text text
        datetime timestamp
        bool is_read
    }
```

## Ограничения целостности

- `Review`: уникальная пара `(user, candle)` — один отзыв на свечу от пользователя.
- `Favorite`: уникальная пара `(user, candle)`.
- `Cart`: OneToOne с User — одна корзина на пользователя.
- `Candle.category`: PROTECT — нельзя удалить категорию с товарами.
- `Candle.author`: SET_NULL — при удалении автора свеча сохраняется."""

API_SPECIFICATION = """Базовый URL: `http://127.0.0.1:8000/api/`  
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
| `ws://host/ws/chat/{chat_id}/` | Сообщения чата |"""

WEBSOCKET_SETUP = """## Технологии

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

Для разработки `runserver` с Channels также поддерживает WebSocket."""

TESTING_REPORT = """## 1. Модульное тестирование (backend)

**Инструмент:** pytest, pytest-django, APIClient.

**Файл:** `backend/tests/test_api.py`

| № | Тест | Ожидание | Результат |
|---|------|----------|-----------|
| 1 | `test_candles_list_public` | GET /api/candles/ → 200 | ✅ PASS |
| 2 | `test_register_login_create_candle` | регистрация, login, POST candle, GET mine | ✅ PASS |
| 3 | `test_favorites_toggle` | toggle избранного on/off | ✅ PASS |

**Запуск:**
```bash
cd backend
python -m pytest -v
```

## 2. Интеграционное тестирование

| Сценарий | Слои | Статус |
|----------|------|--------|
| Регистрация → вход → профиль | React + API + БД | ✅ ручная проверка |
| Каталог с пагинацией и поиском | React Query + API | ✅ |
| Добавление в корзину → заказ | Zustand + API | ✅ |
| WebSocket уведомления | Channels + hook | ✅ ручная проверка |

## 3. Системное тестирование

| Use Case | Шаги | Результат |
|----------|------|-----------|
| UC-01 Регистрация | /register → форма → redirect | OK |
| UC-02 Вход | /login → JWT → каталог | OK |
| UC-03 Просмотр каталога | фильтр, поиск, пагинация | OK |
| UC-04 Создание свечи | /candles/new → mine | OK |
| UC-05 Заказ | корзина → orders | OK |
| UC-06 Отзыв | детальная страница → отзыв | OK |

## 4. Нагрузочное тестирование WebSocket

Для полной сдачи по МУ рекомендуется добавить скрипт на `websockets` / `locust` с 50+ одновременными соединениями. В текущей версии выполнена ручная проверка 2–3 клиентов.

## 5. Выводы

Ключевые компоненты API покрыты автоматическими тестами. Интеграция frontend-backend проверена вручную по основным сценариям. Критических дефектов не выявлено."""

USER_GUIDE = """## Требования

- Браузер: Chrome, Firefox, Edge (актуальная версия)
- Backend: http://127.0.0.1:8000
- Frontend: http://127.0.0.1:5173

## Регистрация и вход

1. Откройте http://127.0.0.1:5173/register
2. Заполните имя пользователя, email, пароль (дважды)
3. Нажмите «Зарегистрироваться»
4. Войдите через http://127.0.0.1:5173/login

## Просмотр каталога

- Главная страница и раздел **Каталог** — список свечей
- Используйте поиск и фильтр по категориям
- Нажмите на карточку для детальной страницы

## Покупка

1. На странице свечи нажмите «В корзину»
2. Перейдите в **Корзину**
3. Нажмите «Оформить заказ»
4. Заказ появится в разделе **Заказы**

## Свои свечи (для авторов)

1. Войдите в аккаунт
2. **Мои свечи** → «Добавить свечу»
3. Заполните название, описание, цену, категорию
4. Редактирование и удаление — только своих публикаций

## Избранное и отзывы

- Кнопка «♥» на карточке — добавить в избранное
- На детальной странице — оставить отзыв (оценка 1–5 и комментарий)
- Новые отзывы других пользователей появляются без перезагрузки (WebSocket)

## Профиль

Раздел **Профиль** — просмотр и редактирование данных учётной записи.

## Уведомления

При авторизации подключается WebSocket; новые уведомления отображаются в интерфейсе.

## API для разработчиков

Swagger: http://127.0.0.1:8000/api/docs/"""
