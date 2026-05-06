@echo off
chcp 65001 > nul
TITLE 一鍵自動翻譯 PDF

cd /d "%~dp0"

echo ========================================================
echo               PDF 一鍵自動翻譯工具
echo     目標語言: 繁體中文 ^| 翻譯引擎: Google (免費)
echo ========================================================
echo.

if not exist "input" mkdir "input"
if not exist "output" mkdir "output"

set count=0
for %%A in ("input\*.pdf") do set /a count+=1

if %count%==0 (
    echo [提示] 尚未偵測到需要翻譯的 PDF 檔案！
    echo 系統正在為您開啟「input」資料夾...
    echo 請將要翻譯的 PDF 放入後，關閉視窗並按任意鍵繼續。
    echo.
    start "" "%~dp0input"
    pause
)

set count=0
for %%A in ("input\*.pdf") do set /a count+=1
if %count%==0 (
    echo [錯誤] 仍然沒有偵測到 PDF 檔案，程式即將退出。
    pause
    exit /b 1
)

echo [進度] 偵測到 %count% 個 PDF 檔案，準備開始...
echo.

set PYTHON_EXE=%~dp0build\runtime\python.exe
set SCRIPT=%~dp0auto_translate.py
set INPUT_DIR=%~dp0input
set OUTPUT_DIR=%~dp0output

"%PYTHON_EXE%" "%SCRIPT%" "%INPUT_DIR%" "%OUTPUT_DIR%"

echo.
echo ========================================================
echo 翻譯完畢！正在為您開啟結果資料夾...
echo ========================================================
start "" "%OUTPUT_DIR%"
pause
