@echo off
setlocal enabledelayedexpansion

:: バッチファイルのあるディレクトリに作業ディレクトリを変更
cd /d "%~dp0"

:: Pythonスクリプトのパスを指定
set SCRIPT_PATH=./translate_srt.py

:: 引数（ドラッグ&ドロップされたファイルのパス）をチェック
if "%~1"=="" (
    echo ファイルが指定されていません。
    goto :eof
)

:: Pythonコマンドとスクリプトのパスを使用してPythonスクリプトを実行
python translate_srt.py "%~1"

if %ERRORLEVEL% neq 0 pause