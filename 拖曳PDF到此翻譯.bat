@echo off
chcp 65001 > nul
TITLE 拖曳 PDF 自動翻譯工具

cd /d "%~dp0"

if "%~1"=="" (
    echo ========================================================
    echo              拖曳 PDF 自動翻譯工具
    echo ========================================================
    echo.
    echo [使用方式] 請將 PDF 檔案直接拖曳到這個圖示上面放開！
    echo            可以一次拖曳多個 PDF 檔案。
    echo.
    pause
    exit /b
)

if not exist "output" mkdir "output"

echo ========================================================
echo              拖曳 PDF 自動翻譯工具
echo     目標語言: 繁體中文 ^| 翻譯引擎: Google (免費)
echo ========================================================
echo.

set PYTHON_EXE=%~dp0build\runtime\python.exe
set SCRIPT=%~dp0auto_translate_single.py
set OUTPUT_DIR=%~dp0output

:loop
if "%~1"=="" goto done
echo --------------------------------------------------------
echo 正在翻譯: %~nx1
"%PYTHON_EXE%" "%SCRIPT%" "%~1" "%OUTPUT_DIR%"
if errorlevel 1 (
    echo [警告] 翻譯失敗，請查看上方錯誤訊息
) else (
    echo [完成] 翻譯成功！
)
echo.
shift
goto loop

:done
echo ========================================================
echo 所有檔案翻譯完畢！正在為您開啟結果資料夾...
echo ========================================================
start "" "%OUTPUT_DIR%"
pause
