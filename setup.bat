@echo off

rem Setup Python virtual environment
set "SCRIPT_DIR=%~dp0"
set "VENV_DIR=%SCRIPT_DIR%venv"

echo Building the virtual environment...
if not exist "%VENV_DIR%" (
    python -m venv "%VENV_DIR%"
)
echo Installing Libraries..."%VENV_DIR%\Scripts\python.exe" -m pip install --upgrade pip
"%VENV_DIR%\Scripts\pip.exe" install -r "%SCRIPT_DIR%requirements.txt"
echo Generating setting file...
if not exist settings.py (
    echo DEEPL_API_KEY = "xxxxxxxx-xxxx-......:fx" > settings.py
) else (
    echo settings.py already exists.
)
pause