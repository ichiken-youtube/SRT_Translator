@echo off
setlocal enabledelayedexpansion

:: バッチファイルのあるディレクトリに作業ディレクトリを変更
cd /d "%~dp0"

:: 引数（ドラッグ&ドロップされたファイルのパス）をチェック
if "%~1"=="" (
    echo File not specified.
    python translate_srt.py
) else (
    python translate_srt.py "%~1"
)

if %ERRORLEVEL% neq 0 pause