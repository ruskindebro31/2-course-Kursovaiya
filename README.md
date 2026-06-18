# Candels — интернет-магазин свечей ручной работы

Курсовой проект (траектория В): Django REST API + React SPA + JWT + WebSocket.

## Структура

```
backend/     — Django REST API
frontend/    — React SPA (Vite)
docs/        — документация курсового проекта (МУ, траектория В)
```

## Документация

Пояснительная записка: [docs/docx/ПОЯСНИТЕЛЬНАЯ_ЗАПИСКА.docx](docs/docx/ПОЯСНИТЕЛЬНАЯ_ЗАПИСКА.docx) (~60 стр., траектория В, ГОСТ)

## Запуск

База данных по умолчанию — **SQLite** (`backend/db.sqlite3`). PostgreSQL подключается только при заданной переменной `POSTGRES_HOST`.

### Backend

Требуется **Python 3.11–3.13** (не используйте 3.14 — админ-панель Django на нём не работает).

```bash
cd backend
py -3.13 -m venv venv313
venv313\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata demo_catalog
python manage.py seed_demo_catalog
python manage.py runserver
```

> Если раньше использовался `venv` на Python 3.14 — удалите папку `venv` и создайте `venv313` как выше. Иначе админ-панель выдаёт ошибку `'super' object has no attribute 'dicts'`.

- API: http://127.0.0.1:8000/api/
- Swagger: http://127.0.0.1:8000/api/docs/

### Frontend

```bash
cd frontend
npm install
npm run dev
```

- SPA: http://127.0.0.1:5173

### Админ-панель Django

1. Создайте суперпользователя (один раз):

```bash
cd backend
venv313\Scripts\activate
python manage.py createsuperuser
```

2. Запустите backend (`python manage.py runserver`).

3. Откройте в браузере: **http://127.0.0.1:8000/admin/**

4. Войдите логином и паролем из `createsuperuser`.

В админке можно редактировать свечи, категории, заказы, пользователей и отзывы.

Скопируйте `.env.example` в `.env` при необходимости.

## Основные возможности

- Каталог свечей: пагинация, поиск, фильтр по категориям
- JWT: регистрация, вход, обновление токена, профиль
- Свои публикации (свечи): создание, редактирование, удаление
- Избранное и отзывы с оптимистичным обновлением UI
- WebSocket: уведомления и отзывы в реальном времени
- Корзина и оформление заказа

## Тесты

```bash
cd backend && python -m pytest -v
cd frontend && npm test
```

## Статистика разработки

| Метрика | Значение |
|---------|----------|
| Всего коммитов | 14 |
| Период разработки | 27.05.2026 — 17.06.2026 |
| Репозиторий | https://github.com/ruskindebro31/2-course-Kursovaiya |
| Траектория | В (Django REST + React + JWT + WebSocket) |
| Стек | Django 4.2, DRF, Channels, React 19, Vite, TanStack Query |
