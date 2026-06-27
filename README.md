# Candels — интернет-магазин свечей ручной работы

Курсовой проект (траектория В): Django REST API + React SPA + JWT + WebSocket.

## Структура

```
backend/     — Django REST API
frontend/    — React SPA (Vite)
docs/        — документация курсового проекта (МУ, траектория В)
```

## Документация

[Пояснительная записка](docs/ПЗ_Рашевский.docx) · [docs/README.md](docs/README.md)

## Запуск

База данных по умолчанию — **SQLite** (`backend/db.sqlite3`). PostgreSQL подключается только при заданной переменной `POSTGRES_HOST`.

### Backend

Требуется **Python 3.11–3.13** (не используйте 3.14 — админ-панель Django на нём не работает).

```bash
cd backend
py -3.13 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata demo_catalog
python manage.py seed_demo_catalog
python manage.py runserver
```

Или на Windows одной командой (соберёт frontend и запустит сервер):

```bash
cd backend
runserver.bat
```

> **Важно:** не используйте Python 3.14. При ошибке `'super' object has no attribute 'dicts'` удалите папку `venv` и выполните `py -3.13 -m venv venv` заново.

- **Сайт (главная Home):** http://127.0.0.1:8000/
- API: http://127.0.0.1:8000/api/
- Swagger: http://127.0.0.1:8000/api/docs/

Перед первым запуском соберите frontend (или используйте `runserver.bat` — он делает это автоматически):

```bash
cd frontend
npm install
npm run build
```

### Frontend (режим разработки)

```bash
cd frontend
npm install
npm run dev
```

- Dev-сервер: http://127.0.0.1:5173 (запросы `/api/` и WebSocket проксируются на backend :8000)

### Админ-панель Django

1. Создайте суперпользователя (один раз):

```bash
cd backend
venv\Scripts\activate
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
| Всего коммитов | 26 |
| Период разработки | 27.05.2026 — 27.06.2026 |
| Средняя частота | ~4,3 коммита/неделю |
| Репозиторий | https://github.com/ruskindebro31/2-course-Kursovaiya |
| Траектория | В (Django REST + React + JWT + WebSocket) |
| Стек | Django 4.2, DRF, Channels, React 19, Vite, TanStack Query |
