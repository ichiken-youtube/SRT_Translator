@echo off
setlocal enabledelayedexpansion

:: バッチファイルのあるディレクトリに作業ディレクトリを変更
cd /d "%~dp0"

:: 引数（ドラッグ&ドロップされたファイルのパス）をチェック
if "%~1"=="" (
    echo File not specified.
    call .\venv\Scripts\python.exe .\translate_srt.py %~dp0
) else (
    call .\venv\Scripts\python.exe .\translate_srt.py %~dp0 "%~1"
)

if %ERRORLEVEL% neq 0 pause