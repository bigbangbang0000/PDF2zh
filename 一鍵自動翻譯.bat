@echo off
chcp 65001 > nul
set PYTHONIOENCODING=utf-8
TITLE 一鍵自動翻譯 PDF 工具

cd /d "%~dp0"

echo ========================================================
echo               PDF 一鍵自動翻譯工具
echo ========================================================
echo.

if not exist "input" mkdir "input"
if not exist "output" mkdir "output"

set count=0
for %%A in ("input\*.pdf") do set /a count+=1

if %count%==0 (
    echo [提示] 尚未偵測到需要翻譯的 PDF 檔案！
    echo 系統即將自動開啟「input」資料夾。
    echo 請將你要翻譯的 PDF 檔案放入該資料夾中。
    echo.
    start "" "input"
    echo 請在放入檔案後，按任意鍵繼續...
    pause
)

set count=0
for %%A in ("input\*.pdf") do set /a count+=1
if %count%==0 (
    echo [錯誤] 仍然沒有偵測到 PDF 檔案，程式即將退出。
    pause
    exit /b
)

echo.
echo [進度] 偵測到 %count% 個 PDF 檔案，開始自動翻譯...
echo.

rem 設定路徑以使用內建環境或全域環境
set PYTHONPATH=%~dp0;%~dp0build\site-packages
set PYTHON_EXE=%~dp0build\runtime\python.exe
set PDF2ZH_EXE=%~dp0build\pdf2zh.exe

for %%f in ("input\*.pdf") do (
    echo --------------------------------------------------------
    echo 正在處理: %%~nxf
    if exist "%PDF2ZH_EXE%" (
        "%PDF2ZH_EXE%" "%%f" --output "output" --service google --lang-out zh-tw --ignore-cache
    ) else if exist "%PYTHON_EXE%" (
        "%PYTHON_EXE%" -m pdf2zh "%%f" --output "output" --service google --lang-out zh-tw --ignore-cache
    ) else (
        python -m pdf2zh "%%f" --output "output" --service google --lang-out zh-tw --ignore-cache
    )
    echo 處理完成: %%~nxf
)

echo --------------------------------------------------------
echo.
echo [完成] 所有檔案翻譯完畢！
echo 系統即將自動為您開啟「output」資料夾以取得翻譯結果...
start "" "output"

pause
