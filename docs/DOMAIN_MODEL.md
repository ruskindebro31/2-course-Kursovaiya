# Доменная модель

```mermaid
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
| Отзыв | Review | рейтинг 1–5; один отзыв на пару user+candle |
