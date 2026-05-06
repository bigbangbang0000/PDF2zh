#!/usr/bin/env python3
import sys
import os
import site
from pathlib import Path

# 強制 UTF-8 輸出
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# 路徑設定
script_dir = Path(__file__).resolve().parent
site_packages = script_dir / "build" / "site-packages"

# 避免本地 pdf2zh.py 遮蔽套件，只加入 site-packages
if site_packages.exists():
    site.addsitedir(str(site_packages))
    sys.path.insert(0, str(site_packages))

try:
    from pdf2zh.gui import demo
    print("[啟動] 正在準備網頁介面...")
    # inbrowser=True 會在伺服器準備好後自動開啟瀏覽器
    demo.launch(inbrowser=True, server_port=7860)
except Exception as e:
    print(f"[錯誤] 無法啟動網頁介面: {e}")
    input("請按 Enter 鍵離開...")
