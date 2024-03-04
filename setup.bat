@echo off
echo Installing Libraries...
pip install PySimpleGUI deepl
echo Generating setting file...
if not exist settings.py (
    echo DEEPL_API_KEY = "xxxxxxxx-xxxx-......:fx" > settings.py
) else (
    echo settings.py already exists.
)
pause