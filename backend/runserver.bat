@echo off
cd /d "%~dp0"
if not exist "venv\Scripts\python.exe" (
  echo Creating venv with Python 3.13...
  py -3.13 -m venv venv
  call venv\Scripts\activate.bat
  pip install -r requirements.txt
) else (
  call venv\Scripts\activate.bat
)
for /f "tokens=*" %%v in ('python -c "import sys; print(sys.version_info[1])"') do set PYMINOR=%%v
if %PYMINOR% GEQ 14 (
  echo.
  echo ERROR: venv uses Python 3.14+. Recreating with Python 3.13...
  rmdir /s /q venv
  py -3.13 -m venv venv
  call venv\Scripts\activate.bat
  pip install -r requirements.txt
)
python manage.py runserver %*
