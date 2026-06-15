# Project Problems



## Current issues



1. ~~PyPI is unavailable from current environment~~ — в этой среде зависимости установлены успешно (`pip install -r requirements.txt`). Если сеть к PyPI недоступна, используйте зеркало или офлайн-колёса.



2. ~~Migrations are not generated yet~~ — добавлены `apps/catalog/migrations/0001_initial.py` и `apps/orders/migrations/0001_initial.py`. Команды: `makemigrations`, `migrate`.



3. ~~Demo fixtures contain products without image files~~ — в `media/products/` добавлены демо-JPEG, в `demo_catalog.json` указаны пути вида `products/...jpg`. Папка `media/products/` разрешена в репозитории через `.gitignore` (остальной `media/` по-прежнему игнорируется).



## Дополнительно исправлено



- **Корзина в сессии:** `Cart.__iter__` больше не мутирует данные сессии (раньше в JSON попадали `Decimal` и модели, из-за чего падало сохранение сессии и тест заказа).



## Структура фронтенда (как у URL сайта)



- `static/core/` — `/` (общий каркас: `base.css`, `home.css`, `menu.js`)

- `static/catalog/` — `/catalog/`

- `static/cart/` — `/cart/`

- `static/orders/` — `/orders/`



Шаблоны: `templates/core/`, `templates/catalog/`, `templates/cart/`, `templates/orders/` (уже совпадали с разделами сайта).



## Demo fixture usage



- Load demo catalog data:

  - `.\.venv\Scripts\python manage.py loaddata apps/catalog/fixtures/demo_catalog.json`


1. после оформления заказа корзина с товарами остается, добавить в корзину статус заказа и функции работы с обрабатываемы заказами, пользователь должен видеть статус заказа