@echo off

call ToolCraftEnv\Scripts\activate.bat

pip install -r requirements.txt >nul 2>&1

start /B python manage.py runserver >nul 2>&1

timeout /t 5 /nobreak >nul

start http://127.0.0.1:8000
