@echo off
chcp 65001 > nul
TITLE PDF2zh 網頁介面

cd /d "%~dp0"

echo ========================================================
echo          PDF2zh 本地網頁翻譯介面
echo ========================================================
echo.
echo [啟動中] 正在載入翻譯模組與模型，請稍候...
echo 載入完成後，系統會自動在你的瀏覽器開啟網頁！
echo.
echo 注意：使用期間請勿關閉這個黑色視窗，關閉即代表停止服務。
echo ========================================================
echo.

set PYTHON_EXE=%~dp0build\runtime\python.exe
set SCRIPT=%~dp0run_gui.py

"%PYTHON_EXE%" "%SCRIPT%"

pause
