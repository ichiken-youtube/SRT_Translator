@echo off
echo Installing Libraries...
pip install PySimpleGUI deepl
echo Generating setting file...
echo DEEPL_API_KEY = "xxxxxxxx-xxxx-......:fx" > settings.py
pause