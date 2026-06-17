# Документация курсового проекта Candels

Траектория **В**: Django REST + React SPA + JWT + WebSocket.

## Пояснительная записка

| Документ | Файл |
|----------|------|
| Пояснительная записка (~60 стр., ГОСТ) | [docx/ПОЯСНИТЕЛЬНАЯ_ЗАПИСКА.docx](docx/ПОЯСНИТЕЛЬНАЯ_ЗАПИСКА.docx) |
| Скриншоты (Приложение Б) | [images/screenshots/](images/screenshots/) |

## Пересборка

```bash
pip install -r docs/requirements-docx.txt
python docs/build_full_report.py
python docs/generate_docx.py
python docs/generate_screenshots.py
```

Результат: `docs/docx/ПОЯСНИТЕЛЬНАЯ_ЗАПИСКА.docx` и копия на рабочем столе `ПОЯСНИТЕЛЬНАЯ_ЗАПИСКА_Candels.docx`. Скрипт проверяет открытие в Microsoft Word.
