#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

MIN_PYTHON = (3, 11)
MAX_PYTHON = (3, 13)


def _check_python_version() -> None:
    version = sys.version_info[:3]
    if version[:2] < MIN_PYTHON or version[:2] > MAX_PYTHON:
        current = '.'.join(map(str, version[:3]))
        print(
            f'\nОшибка: Python {current} не поддерживается.\n'
            'Используйте Python 3.11–3.13 (рекомендуется 3.13).\n\n'
            '  cd backend\n'
            '  py -3.13 -m venv venv\n'
            '  venv\\Scripts\\activate\n'
            '  pip install -r requirements.txt\n'
            '  python manage.py runserver\n',
            file=sys.stderr,
        )
        sys.exit(1)


def main():
    """Run administrative tasks."""
    _check_python_version()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'candels.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
