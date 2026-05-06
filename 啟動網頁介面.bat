@echo off
chcp 65001 > nul
TITLE PDF2zh 網頁介面

cd /d "%~dp0"

echo ========================================================
echo          PDF2zh 本地網頁翻譯介面
echo ========================================================
echo.
echo [啟動中] 正在啟動翻譯介面，請稍候...
echo 啟動完成後，請在瀏覽器中開啟以下網址：
echo.
echo   http://localhost:7860
echo.
echo 注意：關閉此視窗會停止服務。
echo ========================================================
echo.

set PYTHON_EXE=%~dp0build\runtime\python.exe
set SITE_PKG=%~dp0build\site-packages

rem 等2秒後自動開啟瀏覽器
start "" timeout /t 3 /nobreak >nul
start "" "http://localhost:7860"

"%PYTHON_EXE%" -c "import sys, site; site.addsitedir('%SITE_PKG:\=/%'); from pdf2zh.gui import demo; demo.launch(inbrowser=False, server_port=7860)"
