# ER-диаграмма базы данных

```mermaid
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
- `Candle.author`: SET_NULL — при удалении автора свеча сохраняется.
