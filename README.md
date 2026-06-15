# Candels — интернет-магазин свечей ручной работы

Курсовой проект (траектория В): Django REST API + React SPA + JWT + WebSocket.

## Структура

```
backend/     — Django REST API
frontend/    — React SPA (Vite)
docs/        — документация курсового проекта (МУ, траектория В)
```

## Документация

Полный комплект: [docs/README.md](docs/README.md)

**DOCX (ГОСТ 7.32-2017):** [docs/docx/](docs/docx/)

- [Задание на КП](docs/docx/ЗАДАНИЕ_КП.docx) · [Пояснительная записка](docs/docx/ПОЯСНИТЕЛЬНАЯ_ЗАПИСКА.docx)
- [API](docs/docx/API_SPECIFICATION.docx) · [ER](docs/docx/ER_DIAGRAM.docx) · [Архитектура](docs/docx/ARCHITECTURE.docx)

## Запуск

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata demo_catalog
python manage.py runserver
```

- API: http://127.0.0.1:8000/api/
- Swagger: http://127.0.0.1:8000/api/docs/

### Frontend

```bash
cd frontend
npm install
npm run dev
```

- SPA: http://127.0.0.1:5173

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
| Всего коммитов | 5+ |
| Репозиторий | https://github.com/ruskindebro31/2-course-Kursovaiya |
| Траектория | В (Django REST + React + JWT + WebSocket) |
| Стек | Django 4.2, DRF, Channels, React 19, Vite, TanStack Query |
