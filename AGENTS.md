# Candels — инструкции для Odysseus Agent

Проект: интернет-магазин свечей Candels  
Путь: `C:\Users\vacba\Desktop\Candels`  
Docker workspace (Odysseus): `/workspace/candels`  
Траектория: **В** (Django REST + React SPA + JWT + WebSocket)

## Агенты (роли)

| Роль | Skill | Когда использовать |
|------|-------|-------------------|
| Backend | `candels-backend-drf` | DRF API, JWT, Channels |
| Frontend | `candels-frontend-react` | React SPA, React Query |
| QA | `candels-qa` | pytest, Jest, integration |
| DevOps | `candels-devops-review` | Docker, security, review |
| ErrorFixer | `candels-error-fixer` | 404, CORS, баги |

## Порядок работы

1. BackendDeveloper → ErrorFixer
2. FrontendDeveloper → ErrorFixer
3. QAEngineer
4. DevOpsReviewer
5. ErrorFixer (если QA/review fail)

## Конфигурация пайплайна

- `odesseus/agents.yaml` — манифест агентов
- `odesseus/interactions.yaml` — взаимодействия
- `odesseus/fallback.yaml` — fallback при ошибках
- `odesseus/scenarios/candels_trajectory_v.yaml` — сценарий запуска

## Известные баги

См. `PROJECT_PROBLEMS.md`

## Инструменты Odysseus

В Agent mode включить: **Files**, **Shell**, **Skills**, **Web** (по необходимости).
