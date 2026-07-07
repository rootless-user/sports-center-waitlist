@echo off
cd /d "%~dp0"
title Sports Center Waitlist Launcher

netstat -ano | findstr ":5000" | findstr "LISTENING" >nul
if not errorlevel 1 (
    start "" "http://127.0.0.1:5000"
    exit
)

where py >nul 2>&1
if %errorlevel%==0 (
    set PYTHON_CMD=py -3
) else (
    where python >nul 2>&1
    if %errorlevel%==0 (
        set PYTHON_CMD=python
    ) else (
        echo Python is not installed or not added to PATH.
        echo Install Python 3 first.
        pause
        exit /b 1
    )
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv .venv
)

call ".venv\Scripts\activate.bat"

python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing requirements...
    python -m pip install -r requirements.txt
)

start "Sports Center Waitlist Server" cmd /k "call .venv\Scripts\activate.bat && python app.py"

timeout /t 3 >nul

start "" "http://127.0.0.1:5000"

exit