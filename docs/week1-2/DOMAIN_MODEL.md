# ДОМЕННАЯ МОДЕЛЬ
## Candels Project - Интернет-магазин свечей ручной работы

### Общее описание
Доменная модель Candels представляет собой e-commerce систему специализированную на продаже свечей ручной работы, с элементами социальной платформы для мастеров и покупателей.

### Классы доменной модели

#### 1. User (Пользователь)
**Описание**: Основная сущность, представляющая зарегистрированного пользователя системы.

**Атрибуты**:
- id: Integer (первичный ключ)
- email: String (уникальный, обязательный)
- username: String (уникальный, обязательный)
- password: String (хэшированный, обязательный)
- first_name: String (обязательный)
- last_name: String (обязательный)
- role: String (покупатель/мастер/админ)
- is_active: Boolean (по умолчанию true)
- is_staff: Boolean (по умолчанию false)
- is_superuser: Boolean (по умолчанию false)
- date_joined: DateTime (автоматически)
- last_login: DateTime (автоматически)

**Методы**:
- get_full_name(): String
- get_short_name(): String
- has_perm(perm, obj=None): Boolean
- has_module_perms(app_label): Boolean
- is_master(): Boolean
- is_customer(): Boolean

#### 2. Profile (Профиль)
**Описание**: Расширенная информация о пользователе.

**Атрибуты**:
- id: Integer (первичный ключ)
- user: ForeignKey(User) (один к одному)
- avatar: ImageField (опционально)
- bio: TextField (опционально)
- phone: String (опционально)
- shipping_address: TextField (адрес доставки)
- billing_address: TextField (платежный адрес)
- notification_settings: JSON (настройки уведомлений)
- preferences: JSON (пользовательские предпочтения)
- master_specialization: String (специализация мастера)
- master_portfolio: JSON (портфолио мастера)
- created_at: DateTime (автоматически)
- updated_at: DateTime (автоматически)

**Методы**:
- get_avatar_url(): String
- get_notification_preference(type): Boolean
- is_master_profile(): Boolean

#### 3. Category (Категория)
**Описание**: Классификация свечей по типам.

**Атрибуты**:
- id: Integer (первичный ключ)
- name: String (обязательный)
- description: TextField (опционально)
- slug: String (уникальный)
- icon: String (опционально)
- is_active: Boolean (по умолчанию true)
- created_at: DateTime (автоматически)

**Методы**:
- get_candle_count(): Integer
- get_active_candles(): QuerySet

#### 4. Candle (Свеча)
**Описание**: Основной продукт системы - свеча ручной работы.

**Атрибуты**:
- id: Integer (первичный ключ)
- name: String (обязательный)
- description: TextField (обязательный)
- master: ForeignKey(User) (мастер-создатель)
- category: ForeignKey(Category) (обязательный)
- price: Decimal (обязательный)
- currency: String (по умолчанию "RUB")
- stock_quantity: Integer (количество в наличии)
- weight: Decimal (вес в граммах)
- dimensions: JSON (размеры: длина, ширина, высота)
- burn_time: Integer (время горения в часах)
- materials: JSON (используемые материалы)
- fragrances: JSON (ароматы)
- colors: JSON (цвета)
- is_customizable: Boolean (возможность персонализации)
- photos: JSON (список фотографий)
- is_published: Boolean (по умолчанию false)
- views_count: Integer (по умолчанию 0)
- created_at: DateTime (автоматически)
- updated_at: DateTime (автоматически)
- published_at: DateTime (опционально)

**Методы**:
- get_absolute_url(): String
- increment_view_count(): void
- get_review_count(): Integer
- get_average_rating(): Decimal
- get_main_photo(): String
- is_in_stock(): Boolean

#### 5. Order (Заказ)
**Описание**: Заказ покупателя на покупку свечей.

**Атрибуты**:
- id: Integer (первичный ключ)
- customer: ForeignKey(User) (покупатель)
- items: JSON (список товаров в заказе)
- total_amount: Decimal (общая сумма)
- status: String (новый, подтвержден, отправлен, доставлен, отменен)
- shipping_address: TextField (адрес доставки)
- billing_address: TextField (платежный адрес)
- payment_method: String (способ оплаты)
- shipping_method: String (способ доставки)
- tracking_number: String (номер отслеживания)
- created_at: DateTime (автоматически)
- updated_at: DateTime (автоматически)

**Методы**:
- get_item_count(): Integer
- get_status_display(): String
- can_be_cancelled(): Boolean
- update_total_amount(): void

#### 6. OrderItem (Элемент заказа)
**Описание**: Детализация содержимого заказа.

**Атрибуты**:
- id: Integer (первичный ключ)
- order: ForeignKey(Order) (обязательный)
- candle: ForeignKey(Candle) (обязательный)
- quantity: Integer (обязательный)
- price: Decimal (цена на момент заказа)

#### 7. Review (Отзыв)
**Описание**: Отзывы покупателей о свечах.

**Атрибуты**:
- id: Integer (первичный ключ)
- candle: ForeignKey(Candle) (обязательный)
- customer: ForeignKey(User) (обязательный)
- rating: Integer (1-5 звезд)
- comment: TextField (обязательный)
- is_verified_purchase: Boolean (подтвержденная покупка)
- is_active: Boolean (по умолчанию true)
- created_at: DateTime (автоматически)
- updated_at: DateTime (автоматически)

**Методы**:
- get_rating_stars(): String

#### 8. CustomOrder (Персонализированный заказ)
**Описание**: Запрос на создание индивидуальной свечи.

**Атрибуты**:
- id: Integer (первичный ключ)
- customer: ForeignKey(User) (обязательный)
- master: ForeignKey(User) (мастер)
- base_candle: ForeignKey(Candle) (базовая свеча)
- requirements: TextField (требования к персонализации)
- preferred_fragrances: JSON (предпочитаемые ароматы)
- preferred_colors: JSON (предпочитаемые цвета)
- budget: Decimal (бюджет клиента)
- deadline: DateTime (желаемый срок)
- status: String (новый, в работе, готов, отменен)
- estimated_price: Decimal (ориентировочная цена)
- created_at: DateTime (автоматически)
- updated_at: DateTime (автоматически)

#### 9. Cart (Корзина)
**Описание**: Временное хранение выбранных товаров.

**Атрибуты**:
- id: Integer (первичный ключ)
- user: ForeignKey(User) (опционально, для авторизованных)
- session_key: String (для гостей)
- items: JSON (список товаров)
- created_at: DateTime (автоматически)
- updated_at: DateTime (автоматически)

#### 10. Notification (Уведомление)
**Описание**: Система уведомлений пользователей.

**Атрибуты**:
- id: Integer (первичный ключ)
- recipient: ForeignKey(User) (обязательный)
- actor: ForeignKey(User) (кто вызвал уведомление)
- verb: String (действие: 'ordered', 'reviewed', 'custom_ordered', и т.д.)
- target_content_type: ForeignKey(ContentType)
- target_object_id: Integer
- target: GenericForeignKey
- is_read: Boolean (по умолчанию false)
- created_at: DateTime (автоматически)

### Связи между классами

#### Ассоциации:
1. **User** 1 ↔ 1 **Profile** (один пользователь - один профиль)
2. **User** 1 ↔ N **Candle** (один мастер - много свечей)
3. **Category** 1 ↔ N **Candle** (одна категория - много свечей)
4. **User** 1 ↔ N **Order** (один покупатель - много заказов)
5. **Order** 1 ↔ N **OrderItem** (один заказ - много элементов)
6. **Candle** 1 ↔ N **OrderItem** (одна свеча - много заказов)
7. **User** 1 ↔ N **Review** (один покупатель - много отзывов)
8. **Candle** 1 ↔ N **Review** (одна свеча - много отзывов)
9. **User** 1 ↔ N **CustomOrder** (один покупатель - много персонализированных заказов)
10. **User** 1 ↔ N **Notification** (один пользователь - много уведомлений)

#### Наследование:
- **User** ← **Master** (мастер - специализация пользователя)
- **User** ← **Customer** (покупатель - специализация пользователя)
- **User** ← **Admin** (администратор - специализация пользователя)

### Ограничения целостности

#### Бизнес-правила:
1. Email пользователя должен быть уникальным
2. Название свечи не может быть пустым
3. Цена свечи должна быть положительной
4. Количество в наличии не может быть отрицательным
5. Оценка в отзыве должна быть от 1 до 5
6. Покупатель может оставить отзыв только после покупки
7. Мастер может добавлять свечи только после подтверждения статуса мастера

#### Технические ограничения:
1. Максимальная длина username: 150 символов
2. Максимальная длина названия свечи: 200 символов
3. Размер изображений ограничен 10MB
4. Поддерживаемые форматы изображений: JPEG, PNG, WEBP
5. Максимальное количество фотографий для одной свечи: 10

### Диаграмма классов (текстовое представление)