#!/usr/bin/env python3
"""
單一 PDF 翻譯腳本（供拖曳 bat 呼叫）
用法: python auto_translate_single.py <pdf_path> <output_dir>
"""
import sys
import os
import site
from pathlib import Path

# ── 強制 UTF-8 輸出 ────────────────────────────────────────────────────
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# ── 路徑設定 ──────────────────────────────────────────────────────────
script_dir    = Path(__file__).resolve().parent
site_packages = script_dir / "build" / "site-packages"

# 注意：不能把 script_dir 加入 path，否則本地 pdf2zh.py 會遮蔽套件
if site_packages.exists():
    site.addsitedir(str(site_packages))
    sys.path.insert(0, str(site_packages))

# ── 翻譯設定 ──────────────────────────────────────────────────────────
LANG_IN  = "en"
LANG_OUT = "zh-TW"
SERVICE  = "google"
THREADS  = 4

def main():
    if len(sys.argv) < 2:
        print("[錯誤] 請提供 PDF 路徑")
        sys.exit(1)

    pdf_path   = Path(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else script_dir / "output"

    if not pdf_path.exists():
        print(f"[錯誤] 找不到檔案: {pdf_path}")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"  翻譯中: {pdf_path.name}")
    print(f"  語言: {LANG_IN} -> {LANG_OUT} / 引擎: {SERVICE}")

    try:
        from pdf2zh.high_level import translate
        from pdf2zh.doclayout import OnnxModel
    except ImportError as e:
        print(f"[錯誤] 無法載入 pdf2zh: {e}")
        sys.exit(1)

    print("[準備] 載入版面辨識模型...")
    model = OnnxModel.load_available()

    translate(
        files=[str(pdf_path)],
        output=str(output_dir),
        lang_in=LANG_IN,
        lang_out=LANG_OUT,
        service=SERVICE,
        thread=THREADS,
        model=model,
    )
    print(f"  [成功] 輸出: {output_dir / (pdf_path.stem + '-mono.pdf')}")

if __name__ == "__main__":
    main()
