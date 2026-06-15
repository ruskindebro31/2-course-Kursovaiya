#!/usr/bin/env python3
import os

def check_project_structure():
    """Проверка структуры проекта Candels"""
    
    print("Проверка структуры проекта Candels...")
    print("=" * 50)
    
    # Проверка backend структуры
    backend_files = [
        "backend/manage.py",
        "backend/requirements.txt",
        "backend/users/models.py",
        "backend/users/views.py",
        "backend/users/serializers.py",
        "backend/users/urls.py",
        "backend/news/models.py",
        "backend/news/views.py",
        "backend/news/serializers.py",
        "backend/news/urls.py",
        "backend/candels/settings.py",
        "backend/candels/urls.py"
    ]
    
    print("Backend структура:")
    for file_path in backend_files:
        full_path = f"/app/data/candels/{file_path}"
        if os.path.exists(full_path):
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} (отсутствует)")
    
    print("\nFrontend структура:")
    frontend_files = [
        "frontend/package.json",
        "frontend/src/App.js",
        "frontend/src/index.js"
    ]
    
    for file_path in frontend_files:
        full_path = f"/app/data/candels/{file_path}"
        if os.path.exists(full_path):
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} (отсутствует)")
    
    print("\nДокументация:")
    docs_files = [
        "docs/PROJECT_PLAN.md",
        "README.md"
    ]
    
    for file_path in docs_files:
        full_path = f"/app/data/candels/{file_path}"
        if os.path.exists(full_path):
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} (отсутствует)")

if __name__ == "__main__":
    check_project_structure()
