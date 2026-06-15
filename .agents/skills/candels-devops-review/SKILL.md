---
name: candels-devops-review
description: DevOps-проверка Candels — Docker, CORS, security, deployment checklist
version: 1.0.0
category: devops
tags: [docker, security, review, candels]
status: published
confidence: 0.85
source: taught
---

## When to Use

Когда нужно проверить готовность Candels к сдаче/деплою: Docker, безопасность, CORS, документация.

## Procedure

1. Проверить наличие: docker-compose.yml, Dockerfile, frontend/Dockerfile, .env.example.
2. docker-compose должен поднимать: django, react, postgres, redis (Channels).
3. SECRET_KEY не захардкожен — только из .env.
4. DEBUG=False для production, ALLOWED_HOSTS настроен.
5. CORS_ALLOWED_ORIGINS содержит frontend URL.
6. JWT: ROTATE_REFRESH_TOKENS=True, ACCESS 30 min, REFRESH 1 day.
7. OpenAPI/schema доступен на `/api/schema/` или swagger.
8. README.md содержит Git-статистику (требование МУ).
9. Code review: select_related, permissions, no eval/exec.
10. Выдать отчёт: approved/rejected + issues по severity.

## Pitfalls

- InMemoryChannelLayer только для dev; production — Redis.
- Не коммитить .env с секретами.

## Verification

- `docker compose up --build` поднимает все сервисы.
- DevOps checklist: все пункты green или documented exceptions.
