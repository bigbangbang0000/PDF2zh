@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
TITLE 拖曳 PDF 自動翻譯工具

cd /d "%~dp0"

if "%~1"=="" (
    echo ========================================================
    echo               拖曳 PDF 自動翻譯工具
    echo ========================================================
    echo.
    echo [提示] 請直接將 PDF 檔案「拖曳」到這個批次檔圖示上！
    echo 不要雙擊執行此檔案。
    echo.
    pause
    exit /b
)

if not exist "output" mkdir "output"

rem 設定路徑以使用內建環境或全域環境
set PYTHONPATH=%~dp0;%~dp0build\site-packages
set PYTHON_EXE=%~dp0build\runtime\python.exe
set PDF2ZH_EXE=%~dp0build\pdf2zh.exe

echo ========================================================
echo                 開始自動翻譯
echo ========================================================
echo.

:loop
if "%~1"=="" goto end
echo 正在處理: "%~nx1"
if exist "%PDF2ZH_EXE%" (
    "%PDF2ZH_EXE%" "%~1" --output "output" --service google --lang-out zh-tw --ignore-cache
) else if exist "%PYTHON_EXE%" (
    "%PYTHON_EXE%" -m pdf2zh "%~1" --output "output" --service google --lang-out zh-tw --ignore-cache
) else (
    python -m pdf2zh "%~1" --output "output" --service google --lang-out zh-tw --ignore-cache
)
echo 處理完成: "%~nx1"
echo --------------------------------------------------------
shift
goto loop

:end
echo.
echo [完成] 所有檔案翻譯完畢！
echo 系統即將自動為您開啟「output」資料夾以取得翻譯結果...
start "" "output"

pause
