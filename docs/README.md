# Документация курсового проекта Candels

Траектория **В**: Django REST + React SPA + JWT + WebSocket.

## Пояснительная записка (DOCX, ГОСТ 7.32-2017)

| Документ | Файл |
|----------|------|
| Пояснительная записка (~50–60 стр.) | [docx/ПОЯСНИТЕЛЬНАЯ_ЗАПИСКА.docx](docx/ПОЯСНИТЕЛЬНАЯ_ЗАПИСКА.docx) |
| Копия для сдачи | [docx/ПЗ_Рашевский.docx](docx/ПЗ_Рашевский.docx) |

## Пересборка

```bash
pip install -r docs/requirements-docx.txt
python docs/build_full_report.py
python docs/generate_docx.py
python docs/generate_git_charts.py
```

Исходник Markdown (`ПОЯСНИТЕЛЬНАЯ_ЗАПИСКА.md`) хранится локально (в `.gitignore`).
